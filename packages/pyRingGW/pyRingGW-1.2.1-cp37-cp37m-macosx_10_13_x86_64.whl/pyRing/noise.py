# -*- coding: utf-8 -*-
#Standard python imports
from __future__        import division
from io                import StringIO
from scipy.interpolate import interp1d
from scipy.linalg      import inv, toeplitz
from scipy.signal      import butter, filtfilt, welch, tukey, decimate
from scipy.stats       import kstest, multivariate_normal
import matplotlib.mlab as mlab, matplotlib.pyplot as plt, numpy as np, os, sys, warnings

#LVC imports
from gwpy.timeseries import TimeSeries
try:                                      from glue import datafind
except(ImportError, ModuleNotFoundError): pass
import lal

#Package internal imports
from pyRing               import plots
from pyRing.inject_signal import inject_IMR_signal, inject_ringdown_signal
from pyRing.utils         import print_subsection, review_warning, whiten_TD
from pyRing.likelihood    import toeplitz_slogdet

try:                                      from gwmodel.powerspectrum import mesa as mem
except(ImportError, ModuleNotFoundError): pass



################################
# Data manipulation functions. #
################################

def add_injection(on_source_strain, strain, starttime, T, ifo, triggertime, index_trigtime, signal_seglen, kwargs):

    # Inject the NR signal
    if((kwargs['injection-approximant']=='NR') or ('LAL' in kwargs['injection-approximant'])): strain_injection = inject_IMR_signal(     strain.shape[0], starttime, T, ifo, triggertime = triggertime, **kwargs)
    else                                                                                     : strain_injection = inject_ringdown_signal(strain.shape[0], starttime, T, ifo, triggertime = triggertime, **kwargs)

    # Pass as output for the strain the on-source chunk.
    if not((signal_seglen%2)==0): on_source_injection = strain_injection[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
    else:                         on_source_injection = strain_injection[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
    # Add noise on top of injection
    if not(kwargs['zero-noise']):
        sys.stdout.write('* Adding noise on top of injection.\n\n')
        on_source_strain += on_source_injection
    else:
        sys.stdout.write('* Zero noise injection selected.\n\n')
        on_source_strain  = on_source_injection

    return on_source_strain

def excise_nans_from_strain(rawstrain, starttime, T, triggertime, signal_chunk_size, dt, ifo_datafile, download_data_flag):
    
    # Skip, if the data were simulated.
    if(not(ifo_datafile=='') or (download_data_flag)):
        # If there are nans, resize the strain to the longest segment which contains no nans.
        no_nans = 0
        while(no_nans == 0):
            if(np.isnan(rawstrain).any()):
                sys.stdout.write('* Nans found in the data. Resizing strain.\n\n')
                rawstrain, starttime, T = resize_nan_strain(rawstrain, starttime, triggertime, signal_chunk_size, dt)
            else: no_nans = 1

    return rawstrain, starttime, T

def resize_nan_strain(strain, start_time, trig_time, onsource_length, dt):

    srate              = 1./dt
    trig_time_idx      = round((trig_time-start_time)*srate)
    first_idx_onsource = round((trig_time-(onsource_length/2.)-start_time)*srate)
    last_idx_onsource  = round((trig_time+(onsource_length/2.)-start_time)*srate)
    first_nan_index    = None
    last_nan_index     = len(strain)-1

    for j in range(first_idx_onsource, last_idx_onsource): assert not(np.isnan(strain[j])), "Nans present on the onsource chunk, resize the onsource chunk to a segment which does not contain nans."
    for i in range(len(strain)):
        if(first_nan_index == None):
            if(np.isnan(strain[i])):
                first_nan_index = i
        else:
            if not(np.isnan(strain[i])):
                last_nan_index = i-1
                break

    # Since we raise an error in the case where the nans overlap with the onsource chunk, now the only possibility is that the nan block is either to the left (first block below) or to the right (second block below) with respect to the onsource chunk.
    if(last_nan_index < trig_time_idx):
        sys.stdout.write('Nans present in the [{0:.2f}, {1:.2f}]s interval (before signal).\nResizing data to the [{2}, {3}]s interval. Remaining length: {4}s\n'.format(start_time+first_nan_index*dt, start_time+last_nan_index*dt, int(start_time+(last_nan_index+1)*dt), int(start_time+(len(strain))*dt), int((len(strain)-(last_nan_index+1))*dt)))
        
        new_strain     = strain[last_nan_index+1:]
        new_start_time = start_time+(last_nan_index+1)*dt

    else:
        sys.stdout.write('Nans present in the [{0:.2f}, {1:.2f}]s interval (after signal).\nResizing data to the [{2}, {3}]s interval. Remaining length: {4}s\n'.format(start_time+first_nan_index*dt, start_time+last_nan_index*dt, int(start_time), int(start_time+(first_nan_index-1)*dt), int((first_nan_index-1)*dt)))
        
        new_strain     = strain[:first_nan_index-1]
        new_start_time = start_time

    new_T = len(new_strain)*dt
        
    return new_strain, new_start_time, new_T

def bandpass_data(rawstrain, f_min_bp, f_max_bp, srate_dt, bandpassing_flag):

    if(bandpassing_flag):
        # Bandpassing section.
        sys.stdout.write('* Bandpassing the raw strain between [{}, {}] Hz.\n\n'.format(f_min_bp, f_max_bp))

        # Create a fourth order Butterworth bandpass filter between [f_min, f_max] and apply it with the function filtfilt.
        bb, ab = butter(4, [f_min_bp/(0.5*srate_dt), f_max_bp/(0.5*srate_dt)], btype='band')
        strain = filtfilt(bb, ab, rawstrain)
    else:
        sys.stdout.write('* No bandpassing applied.\n\n')
        strain = rawstrain

    return strain

def check_sampling_rate_compatibility(requested_sampling_rate, data_sampling_rate):
    if (requested_sampling_rate > data_sampling_rate): raise ValueError("* You requested a sampling rate higher than the data sampling.")
    else                                             : return

def check_seglen_compatibility(signal_chunk_size, noise_chunk_size, T):
    assert not((noise_chunk_size > T) or (signal_chunk_size > T)), "* Noise ({} s) and signal ({} s) seglens must be shorter than data duration ({})".format(noise_chunk_size, signal_chunk_size, T)
    return

def downsample_data(strain, srate, srate_dt):

    # Check that the sample rate from the data is the same passed in the configuration file. In case they are different, either downsample or throw an error.
    # Set the dt consistently to the requested sampling rate.
    if(srate < srate_dt):
        sys.stdout.write('* Downsampling detector data from {} to {} Hz, decimate factor {}\n\n'.format(srate_dt, srate, int(srate_dt/srate)))
        strain = decimate(strain, int(srate_dt/srate), zero_phase=True)
    else                : pass

    dt = 1./srate
    
    return strain, dt

def chunks_iterator(times, strain, chunksize, avoid=None, window=False, alpha=0.1):
    """
        Divide the data in chunks. Skip the 0th and the last chunks which have filter ringing from downsampling.
    """
    if avoid is None: avoid = times[0]-1e6 # dummy value
    if window: win = tukey(chunksize,alpha=alpha)
    else:      win = np.ones(chunksize)
    #The integer division is needed in case the chunk length in seconds is not a sub-multiple of the total strain length (e.g. after quality veto cuts)
    for j in range(1,len(strain)//chunksize):
        if not times[chunksize*j] < avoid < times[chunksize*(j+1)]: yield strain[chunksize*j:chunksize*(j+1)]*win

def chunks(times, strain, chunksize, trigger_time):
    
    time_chunks_list, data_chunks_list = [], []
    for j in range(1,len(strain)//chunksize):
        
        if not times[chunksize*j] < trigger_time < times[chunksize*(j+1)]:
            data_chunks_list.append(strain[chunksize*j:chunksize*(j+1)])
            time_chunks_list.append(times[chunksize*j:chunksize*(j+1)])
        else: index_trig = j

    return np.array(time_chunks_list), np.array(data_chunks_list), index_trig

def compute_on_off_source_strain(strain, signal_seglen, index_trigtime):

    on_source_mask = np.ones(len(strain), dtype=bool)
    if not((signal_seglen%2)==0):
        on_source_strain = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
        on_source_mask[range(index_trigtime-signal_seglen//2,index_trigtime+signal_seglen//2+1,1)] = False
    else:
        on_source_strain = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
        on_source_mask[range(index_trigtime-signal_seglen//2,index_trigtime+signal_seglen//2,1)]   = False

    off_source_strain = tuple((strain)[on_source_mask])

    return on_source_strain, off_source_strain

def window_onsource_strain(on_source_strain, signal_seglen, noise_seglen, window_onsource_flag, window_flag, alpha_window, truncate):

    if (window_onsource_flag and window_flag):
        if(truncate): print('* Warning: The on-source chunk should not be windowed when truncating data.')
        else        : assert (signal_seglen==noise_seglen), "* If a window is applied, the length of the signal chunk and of the noise chunk must be the same, otherwise with the same Tukey alpha-parameter PSD will be underestimated. Either choose different alphas or equal lengths."
        on_source_window = tukey(signal_seglen, alpha=alpha_window)
        on_source_strain = on_source_strain*on_source_window

    return on_source_strain

def check_chunksizes_consistency(signal_chunk_size, noise_chunk_size, truncate):
    
    if(not(truncate) and not(signal_chunk_size==noise_chunk_size)): print("* Warning: A different chunksize between signal and noise implies an incorrect normalization of the autocorrelation function in the non-truncated case. This configuration should not be used for production runs.")

    return

##########################
# ACF related functions. #
##########################

def acf(y, fft=True, simple_norm=False):

    """
        Returns the autocorrelation function (ACF): R[i] = sum_n x[n]*x[n+i], in the form of an array spanned by the index i.
        
        Computes the ACF using either the standard correlation (with the appropriate normalisation) or the `fft` method. The latter simply exploits the fact that the ACF is a convolution product and that the Fourier transform of a a convolution product is a product in the Fourier domain, see section 'Efficient computation' of 'https://en.wikipedia.org/wiki/Autocorrelation#cite_note-3.
        
        The difference between the two methods is in the treatment of boundary terms. When computing the ACF using the standard correlation, we  'slide' the data vector against a delayed copy of itself, obtaining the correlation at different lags. For all lags except lag=0, part of the 'slided' vector will spill over the boundaries of the fixed vector. In this method, terms outside the vectors boundaries are assigned zeros. This implies that for increasing lag, an increasingly smaller number of terms will contribute, and the variance of large-lag terms grow. Also, the ACF will eventually go to zero, when the maximum lag is reached. When employing the fft method instead, the data are windowed at the boundaries to avoid Gibbs phenomena, and periodic boundary conditions are assumed when applying the Fourier transform, implying a different structure for large lags.
    
        For small lags (compared to the total length of the vector), the portion of the sum which dependent on boundary terms will be small, since the vectors still possess a significant overlap, and the specific method used should not matter (if gaussianity and stationarity assumptions are respected). For this reason, the length of the data on which the ACF is estimated, should always be much larger than the analysis segment length.

    """

    N = len(y)

    # FIXME: the norm option should be applied to both cases and taken out of the fft if-else
    if fft:
        # ACF computation using FFT.
        Y=np.fft.fft(y)
        # We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part is already 0 when coming out of the fft.
        R = np.real(np.fft.ifft(Y*Y.conj()))
        # Divide by an additional factor of 1/N since we are taking two fft and one ifft without unitary normalization, see: https://docs.scipy.org/doc/numpy/reference/routines.fft.html#module-numpy.fft
        acf_normed = R/N
    else:
        # ACF computation without FFT by directly correlating the time series.
        # For real functions, the ACF is symmetric around zero-lag, so take only the second half (the positive lag terms).
        acf_numpy = np.correlate(y, y, mode='full')[N-1:]
        # The `simple norm` version is a biased estimator, but reduces the weight of the terms with large lag, where the ACF variance is larger. The other version is unbiased, but weights more terms with large lags. See arXiv:2107.05609 for references.
        if simple_norm: acf_normed = acf_numpy[:N] / N
        else          : acf_normed = acf_numpy[:N] / (N - np.arange(N))

    return acf_normed

def compute_Welch_PSD(off_source_strain, srate, noise_seglen, psd_window):

    sys.stdout.write('* Computing the one-sided PSD with the Welch method for comparison with the standard ACF.\n\n')
    
    psd_welch, freqs_welch = mlab.psd(off_source_strain, Fs = srate, NFFT = noise_seglen, window = psd_window, sides  = 'onesided')
    df_welch               = np.diff(freqs_welch)[0]

    return psd_welch, freqs_welch, df_welch

def compute_acf_and_whitening_psd(times, strain, starttime, T, srate, triggertime, index_trigtime, dt, window_flag, alpha_window, noise_chunk_size, noise_seglen, signal_seglen, f_min_bp, f_max_bp, fft_acf, freqs_welch, psd_welch, ifo, kwargs):

    # Case where the ACF was pre-computed or the run was already performed.
    if (not(kwargs['acf-{}'.format(ifo)]=='') or (kwargs['run-type']=='post-processing')):
        
        if(not(kwargs['acf-{}'.format(ifo)]=='')):
            assert (fft_acf), "Cannot compute ACF in time domain and load it from file."
            assert (kwargs['psd-{}'.format(ifo)]==''), "Both a PSD and an ACF from file can't be passed."
            acf_file = kwargs['acf-{}'.format(ifo)]
            sys.stdout.write('* Reading ACF from: `{}`.\n\n'.format(acf_file))
        else:
            acf_file = os.path.join(kwargs['output'],'Noise','ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate))
            sys.stdout.write('* Reading ACF from: `{}`.\n\n'.format(acf_file))

        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function, see eq. 7.15 of Maggiore Vol.1
        # We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        time, ACF = np.loadtxt(acf_file, unpack=True)
        dt_acf    = time[1]-time[0]
        assert (dt_acf == dt), "ACF (%r) and data (%r) sampling rates do not agree."%(dt_acf, dt)
        psd_ACF, freqs_acf = 2*np.real(np.fft.rfft(ACF*dt)), np.fft.rfftfreq(len(ACF), d=dt)
        plots.plot_ACF(time        = time,
                       acf         = ACF,
                       label       = '$\mathrm{ACF \,\, from \,\, file}$',
                       output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_acf,
                               psd1        = psd_ACF,
                               label1      = "$\mathrm{PSD \,\, from \,\, loaded ACF}$",
                               freqs2      = freqs_welch,
                               psd2        = psd_welch,
                               label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))

        whitening_PSD = interp1d(freqs_acf, psd_ACF)

    # Case where the PSD was pre-computed.
    elif (not(kwargs['psd-{}'.format(ifo)]=='') and (kwargs['gaussian-noise']=='')):

        # OPTIMISEME: for gaussian noise this is avoided just because of the way injections studies were performed during the review. To be relaxed in post O3a.
        assert (kwargs['acf-{}'.format(ifo)]==''), "Both a PSD and an ACF from file can't be passed."
        psd_file = kwargs['psd-{}'.format(ifo)]
        sys.stdout.write('* PSD was passed. Reading PSD from: `{}` and generating ACF accordingly.\n\n'.format(psd_file))
        if('PESummary' in psd_file):
            psd_datafile = np.genfromtxt(psd_file, names=True)
            freqs_from_file, psd_from_file = psd_datafile['Frequency'], psd_datafile['Strain']
        else:
            freqs_from_file, psd_from_file = np.loadtxt(psd_file, unpack=True)
        if('ASD' in psd_file):
            psd_from_file = psd_from_file*psd_from_file

        # Restrict to sensitive band (needed because BW PSD saturates to ~1 outside sensitive band and it screws up the likelihood)
        f_min_psd       = max(f_min_bp, 20.0)
        f_max_psd       = min(f_max_bp, 2038.0)
        if((f_min_bp < f_min_psd) or (f_max_bp > f_max_psd)): print('* Warning: selected minimum and maximum bandpassing frequencies are outside the hardcoded frequency range in which PSDs are usually well behaved, and the PSD frequency interval has been set to [{}, {}]. Consider changing this behaviour, if required by your analysis.'.format(f_min_psd, f_max_psd))

        psd_from_file   = psd_from_file[  freqs_from_file > f_min_psd]
        freqs_from_file = freqs_from_file[freqs_from_file > f_min_psd]
        psd_from_file   = psd_from_file[  freqs_from_file < f_max_psd]
        freqs_from_file = freqs_from_file[freqs_from_file < f_max_psd]

        # OPTIMISEME: test if leaving the original freq axis does not create issues with the remainder of the code (will probably need to redefine time axis)
        psd_from_file_interp           = interp1d(freqs_from_file, psd_from_file, fill_value='extrapolate', bounds_error=False)
        freqs_default                  = np.fft.rfftfreq(noise_seglen, d = dt)
        df_default                     = np.diff(freqs_default)[0]
        psd_interp                     = psd_from_file_interp(freqs_default)
        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        ACF_psd = 0.5*np.real(np.fft.irfft(psd_interp*df_default))*noise_seglen
        acfs    = [acf(x) for x in chunks_iterator(times, strain, noise_seglen, avoid=triggertime, window=window_flag, alpha=alpha_window)]

        if(kwargs['noise-averaging-method']=='mean'):
            ACF_TD = np.mean(np.array(acfs), axis=0)
        elif(kwargs['noise-averaging-method']=='median'):
            # FIXME: This option gives rise to a junk spectrum. Currently not understood.
            review_warning()
            ACF_TD = np.median(np.array(acfs), axis=0)

        plots.plot_ACF(time        = dt*np.arange(len(ACF_psd)),
                       acf         = ACF_psd,
                       label       = '$\mathrm{ACF \,\, from \,\, file \,\, PSD}$',
                       output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_psd.pdf'.format(ifo)))
        plots.plot_ACF(time        = dt*np.arange(len(ACF_TD)),
                       acf         = ACF_TD,
                       label       = '$\mathrm{time \,\, domain \,\, ACF}$',
                       output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_TD.pdf'.format(ifo)))
        plots.plot_ACF_compare(time1       = dt*np.arange(len(ACF_TD)),
                               acf1        = ACF_TD,
                               label1      = '$\mathrm{time \,\, domain \,\, ACF}$',
                               time2       = dt*np.arange(len(ACF_psd)),
                               acf2        = ACF_psd,
                               label2      = '$\mathrm{ACF \,\, from \,\, PSD}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_ACF_TD_vs_ACF_from_PSD.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_from_file,
                               psd1        = psd_from_file,
                               label1      = '$\mathrm{PSD \,\, from \,\, file}$',
                               freqs2      = freqs_welch,
                               psd2        = psd_welch,
                               label2      = '$\mathrm{Welch, \,\, frequency \,\, domain}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_file_vs_Welch.pdf'.format(ifo)))
        plots.plot_PSD_compare(freqs1      = freqs_from_file,
                               psd1        = psd_from_file,
                               label1      = '$\mathrm{PSD \,\, from \,\, file}$',
                               freqs2      = freqs_default,
                               psd2        = psd_interp,
                               label2      = '$\mathrm{PSD \,\, interpolated}$',
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_file_vs_interp.pdf'.format(ifo)))
        whitening_PSD = psd_from_file_interp
        ACF           = ACF_psd

        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF)), ACF)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_TD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF_TD)), ACF_TD)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_file_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_from_file, psd_from_file)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_Welch_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))

    #Case where the PSD is to be computed following the MaxEnt method.
    elif (not(kwargs['maxent-psd']=='')): ACF, whitening_PSD = compute_maxent_PSD(times, strain, starttime, T, srate, triggertime, index_trigtime, dt, alpha_window, noise_seglen, signal_seglen, fft_acf, freqs_welch, psd_welch, ifo, kwargs)

    #Case where the ACF is computed from the data.
    else:
        if not(kwargs['injection-approximant']==''): sys.stdout.write ('* Although an injection was selected, the ACF is being computed from the strain.\n\n')
        else                                       : sys.stdout.write('* No ACF was passed. Estimating ACF.\n\n')
        acfs = [acf(x, fft=fft_acf, simple_norm=kwargs['acf-simple-norm']) for x in chunks_iterator(times, strain, noise_seglen, avoid=triggertime, window=window_flag, alpha=alpha_window)]

        if(kwargs['noise-averaging-method']=='mean'):
            ACF = np.mean(np.array(acfs), axis=0)
        elif(kwargs['noise-averaging-method']=='median'):
            # FIXME: This option gives rise to a junk spectrum. Currently not understood.
            review_warning()
            ACF = np.median(np.array(acfs), axis=0)

        freqs_default = np.fft.rfftfreq(noise_seglen, d=dt)
        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        psd_ACF       = 2*np.real(np.fft.rfft(ACF*dt))

        plots.plot_ACF(time        = dt*np.arange(len(ACF)),
                       acf         = ACF,
                       label       = '$\mathrm{ACF \,\, TD}$',
                       output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))

        if(kwargs['PSD-investigation']):
            review_warning()
            sys.stdout.write('* Plotting PSDs relative to all chunks.\n\n')
            psds_acf = [2*np.real(np.fft.rfft(single_acf*dt)) for single_acf in acfs]
            plt.figure()
            for single_psd in psds_acf:
                plt.loglog(freqs_default, single_psd)
            plt.xlabel(r"$f\,(Hz)$",        fontsize=18)
            plt.ylabel(r"$S(f)\,(Hz^{-1})$",fontsize=18)
            plt.savefig(os.path.join(kwargs['output'],'Noise','{}_PSD_investigation.pdf'.format(ifo)), bbox_inches='tight')
            exit()

        plots.plot_PSD_compare(freqs1      = freqs_welch,
                               psd1        = psd_welch,
                               label1      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                               freqs2      = freqs_default,
                               psd2        = psd_ACF,
                               label2      = "$\mathrm{time \,\, domain}$",
                               output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))

        if (not(kwargs['psd-{}'.format(ifo)]=='') and not(kwargs['gaussian-noise']=='')):
            # Case where you passed a PSD, generated gaussian noise with it and estimated the PSD from the noise generated. Check if the PSD injected resembles the estimation.
            psd_file = kwargs['psd-{}'.format(ifo)]
            freqs_from_file, psd_from_file = np.loadtxt(psd_file, unpack=True)
            if('ASD' in psd_file): psd_from_file = psd_from_file*psd_from_file
            plots.plot_PSD_compare(freqs1      = freqs_from_file,
                                   psd1        = psd_from_file,
                                   label1      = "$\mathrm{PSD \,\, from \,\, file}$",
                                   freqs2      = freqs_welch,
                                   psd2        = psd_welch,
                                   label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                                   output_path = os.path.join(kwargs['output'],'Noise','{}_PSD_injected.pdf'.format(ifo)))

        if(kwargs['non-stationarity-check']): non_stationarity_check(acfs, dt)

        np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF)), ACF)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))
        np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_from_ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_default, psd_ACF)))

        whitening_PSD = interp1d(freqs_default, psd_ACF)

    return ACF, whitening_PSD

def check_covariance_matrix_inversion_stability(Covariance_matrix_signal, debug, tolerance=1e14):

    # Let's compute the conditioning number and raise a warning in case this starts introducing significant errors in our computations.
    C_inv_debug = inv(Covariance_matrix_signal)
    id          = np.dot(Covariance_matrix_signal, C_inv_debug)
    id_minus_id = np.max(np.absolute(id - np.identity(len(Covariance_matrix_signal[0]))))
    cond_num    = np.linalg.cond(Covariance_matrix_signal)

    if(cond_num > tolerance):
        sys.stdout.write('* WARNING: Covariance matrix conditioning number is {:e}, and exceeds the safety threshold of {:e}, implying possible errors of order 1% or greater in the likelihood computation (since we use double precision, hence ~16 significant digits). Double check your settings, e.g. search for possible data corruption, inconsistency of sampling rate and bandpassing filter, etc. Also, consider trying different covariance inversion methods to improve the numerical stability and verify the robustness of the analysis results (see the `likelihood-method` option). Running with the `debug` option turned on will print additional information.\n\n'.format(cond_num, tolerance))

    if(debug):
        sys.stdout.write('* DEBUG: Covariance matrix maximum inversion error: {:e}\n\n'.format(id_minus_id))
        sys.stdout.write('* DEBUG: Covariance matrix conditioning number: {:e}\n\n'.format(cond_num))

    return

def check_Plancherel_ratio(psd_window_norm, df_welch, psd_welch, dt, ACF, debug):

    # Let's check if Plancherel theorem is verified by our ACF estimate, by using the fact that twice the Fourier transform of the ACF = one-sided PSD (approximately, in the truncated case). Since the psd is the one-sided, we only stored positive values, but Plancherel theorem must be evaluated on both positive and negative frequencies. Also, need to take into account the fact that the window absorbed some power.
    
    FD_term          = psd_window_norm*2.*np.sum(df_welch*psd_welch**2)
    TD_term          = np.sum(dt*(2.*ACF)**2)
    Plancherel_ratio = FD_term/TD_term
    
    if(debug): sys.stdout.write('* DEBUG: Plancherel theorem ratio E(f)/E(t) (expected value: ~1) = {}\n\n'.format(Plancherel_ratio))

    return

def chisquare_computation(ACF, chisquare_flag):

    if (chisquare_flag):
        # Do a check of the reduced chisq, skipping the onsource chunk - useful for checking normalisation.
        Covariance_matrix                = toeplitz(ACF)
        Inverse_Covariance_matrix        = inv(Covariance_matrix)
        Inverse_covariance_matrix_signal = inv(Covariance_matrix_signal)
        chisq                            = [np.einsum('i,ij,j', x, Inverse_Covariance_matrix, x) for x in chunks_iterator(times, strain, noise_seglen, avoid=triggertime, window=window_flag, alpha=alpha_window)]
        sys.stdout.write('* Average reduced chisquare (expected value ~1) = {:.5f}\n\n'.format(np.mean(chisq)/Inverse_Covariance_matrix.shape[0]))

        # A value of onsource chisquare significantly different from 0 indicates that the data in this chunk do not follow the distribution of the noise, which is true if a signal is present.
        sigchisq=np.einsum('i,ij,j', on_source_strain, Inverse_covariance_matrix_signal, on_source_strain)
        sys.stdout.write('* Chisquare on source (expected value >> 1): {}\n\n'.format(sigchisq))

    return

def check_data_gaussianity(times, data, Covariance, signal_seglen, trigger_time, string_output, outdir):

    string_output = string_output.replace('.txt', '')

    # FIXME: this number should be experimented with.
    nbins = 50

    # Split the data in chunks (consistently with the way the ACF was estimated), removing the signal.
    # FIXME: This first step should split the data into signal_seglen chunks, avoiding a large window containing the signal (since the IMR signal is longer than our ringdown analysis seglen).
#    _, data_chunks, _ = chunks(         times, data,        signal_seglen,       trigger_time                               )
    # This second step splits the data into smaller analysis-duration chunks.
    data_chunks       = chunks_iterator(times, data, Covariance.shape[0], avoid=trigger_time, window=False, alpha=0.1)

    # Whiten each chunk.
    cholesky_matrix      = np.linalg.cholesky(Covariance)
    whitened_data_chunks = [whiten_TD(x, cholesky_matrix) for x in data_chunks]
    
    normal_draws         = np.random.normal(size=1000000)

    # Plot whitened data against a normal distribution, to visually check gaussianity.
    plt.figure()
    for x in whitened_data_chunks: plt.hist(x, histtype='step', bins=nbins, stacked=True, fill=False, density=True)
    gaussian_x, bins_gauss, _ = plt.hist(normal_draws, label='Expected distribution', histtype='step', bins=nbins, stacked=True, fill=False, density=True, color='black', linewidth=2.0)
# Work in progress
#    sigma                     = [gaussian_x[i]*(1-gaussian_x[i]) for i in range(len(gaussian_x))]
#    lower, upper              = gaussian_x - sigma, gaussian_x + sigma
#    plt.plot(bins_gauss[:-1], lower, color='black', linewidth=1.7, linestyle='dashed')
#    plt.plot(bins_gauss[:-1], upper, color='black', linewidth=1.7, linestyle='dashed')
    plt.legend(loc='best')
    plt.xlabel('Whitened noise')
    plt.savefig(os.path.join(outdir, 'Noise','Histrogram_whitened_data_{}.pdf'.format(string_output)), bbox_inches='tight')

    # Now let's compute a quantitative measure of gaussianity with zero mean and unit variance.
    KS_p_values, mus, sigmas = [], [], []
    p_value_threshold = 0.01
    
    for x in whitened_data_chunks:
        KS_statistic, p_value = kstest(x, "norm")
        KS_p_values.append(p_value)
        mus.append(np.mean(x))
        sigmas.append(np.std(x, ddof=1))
    KS_p_values   = np.array(KS_p_values)
    mus           = np.array(mus)
    sigmas        = np.array(sigmas)

    mask_outliers = KS_p_values < p_value_threshold
    N_outliers    = len(KS_p_values[mask_outliers])
    len_tot       = len(KS_p_values)
    n, bins, _    = plt.hist(KS_p_values)
    bin_width     = bins[1] - bins[0]
    integral      = bin_width * sum(n)
    duration      = np.diff(times)[0]*Covariance.shape[0]

    plt.figure()
    plt.hist(KS_p_values, histtype='step', bins=nbins, stacked=True, fill=False, color='black', linewidth=2.0)
    plt.axvline(p_value_threshold, label = 'Significance level: {}\nN outliers: {}/{}'.format(p_value_threshold, N_outliers, len_tot), color='darkred', linestyle='dashed', linewidth=1.5)
    plt.xlabel('Kolmogorov–Smirnov p-values')
    plt.title('Integral: {:.6f}'.format(integral))
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(outdir, 'Noise',' histogram_Kolmogorov_Smirnov_test_whitened_data_{}.pdf'.format(string_output)), bbox_inches='tight')

    plt.figure()
    plt.scatter(duration*np.arange(0,len(KS_p_values)), 1-KS_p_values, color='black', marker='x')
    plt.axhline(1-p_value_threshold, label = 'Significance level: {}\nN outliers: {}/{}'.format(p_value_threshold, N_outliers, len_tot), color='darkred', linestyle='dashed', linewidth=1.5)
    plt.xlabel('Time [s]')
    plt.ylabel('Kolmogorov–Smirnov 1 \, - \, p-values')
    plt.ylim([0,1.2])
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(outdir, 'Noise',' scatter_Kolmogorov_Smirnov_test_whitened_data_{}.pdf'.format(string_output)), bbox_inches='tight')

    plt.figure()
    plt.scatter(duration*np.arange(0,len(KS_p_values)), mus, facecolors='none', edgecolors='teal')
    plt.axhline(0.0, label = 'Expected mean', color='darkred', linestyle='dashed', linewidth=1.5)
    plt.xlabel('Time [s]')
    plt.ylabel('$\mu$')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(outdir, 'Noise',' scatter_medians_whitened_data_{}.pdf'.format(string_output)), bbox_inches='tight')

    plt.figure()
    plt.scatter(duration*np.arange(0,len(KS_p_values)), sigmas, facecolors='none', edgecolors='teal')
    plt.axhline(1.0, label = 'Expected standard deviation', color='darkred', linestyle='dashed', linewidth=1.5)
    plt.xlabel('Time [s]')
    plt.ylabel('$\sigma$')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(outdir, 'Noise',' scatter_sigmas_whitened_data_{}.pdf'.format(string_output)), bbox_inches='tight')

    print('* A Kolmogorov–Smirnov test of whitened data chunks gave {}/{} normality outliers (at {} % significance).'.format(N_outliers, len_tot, p_value_threshold*100))

    return

###########################
# Loading data functions. #
###########################

def fetch_data(ifo, tstart, tend, channel=None, path=None, verbose=0, tag=None):

    """
        Fetch data for a particular event

        ifo: IFO name ('H1' etc)
        tstart, tend: start and end time to find
        path: Local path to save file. If file exists it will be read from disk rather than fetched
        channel: Channel to read from frame data. If 'GWOSC' will fetch open data
        verbose: Print some info

        Returns a gwpy.TimeSeries object
    """

    # If file was previously saved, open it.
    if path is not None and os.path.exists(path):
        tseries = TimeSeries.read(path,start=tstart,end=tend)
        if verbose: sys.stdout.write('Reading from local file: `{}`.'.format(path))
        return tseries

    # If not, then see if it is on GWOSC.
    if channel=='GWOSC':
        #When downloading public data, fetch them with the highest possible sampling rate, then pyRing will down-sample internally, if required. This is needed to avoid incompatibilities between GWOSC down-sampling and the pyRing internal one. The actual function used to down-sample is the same, but differences in things like the length of data stretch can affect filtering at the borders and hence the Bayes Factors.
        tseries = TimeSeries.fetch_open_data(ifo, tstart, tend, sample_rate = 16384, verbose=verbose, cache=True, tag=u"{0}".format(tag))
    else:
        # Read from authenticated data.
        if channel is None: raise Exception('Channel not specified when fetching frame data.')
        tseries = TimeSeries.get(channel, tstart, tend, verbose=verbose)
    if path is not None: tseries.write(path)

    return tseries


#FIXME: this function is too big and should be split. Also, it should be a class or a subclass of the detector class, not a function
def load_data(ifo, fname, **kwargs):

    """
        Reads the strain or downloads it using gwpy.
        Computes the ACF either from the directly data or from given file input ACF/PSD.
        Injects a template if requested.
    """

    print_subsection('{}'.format(ifo))

    # Data parameters.
    download_data_flag   = kwargs['download-data']
    ifo_datafile         = kwargs['data-{}'.format(ifo)]
    
    # Time parameters.
    triggertime          = kwargs['trigtime']
    srate                = kwargs['sampling-rate']

    # ACF parameters.
    truncate             = kwargs['truncate']
    fft_acf              = kwargs['fft-acf']
    signal_chunk_size    = kwargs['signal-chunksize']
    noise_chunk_size     = kwargs['noise-chunksize']

    # Band-passing parameters.
    bandpassing_flag     = kwargs['bandpassing']
    f_min_bp             = kwargs['f-min-bp']
    f_max_bp             = kwargs['f-max-bp']
    
    # Windowing parameters.
    window_onsource_flag = kwargs['window-onsource']
    window_flag          = kwargs['window']
    alpha_window         = kwargs['alpha-window']

    # Testing parameters.
    debug                = kwargs['debug']
    chisquare_flag       = kwargs['chisquare-computation']
    
    # Auxiliary derived quantities.
    signal_seglen        = np.int(srate*signal_chunk_size)
    noise_seglen         = np.int(srate*noise_chunk_size)
    
    # Basic sanity checks.
    assert not(triggertime is None), "No triggertime given."
    check_chunksizes_consistency(signal_chunk_size, noise_chunk_size, truncate)


    ####################################
    # Data loading/generation section. #
    ####################################

    # Start to read the data.
    if not(ifo_datafile==''):
        # If a data file is passed, check that no contrasting option (generate gaussian-noise or download data) is passed.
        if (not(kwargs['gaussian-noise']=='')): raise ValueError("If 'gaussian-noise' is selected, no data must be passed.")
        else:
            if not(kwargs['ignore-data-filename']):
                sys.stdout.write("* Warning: The file name is expected to follow GWOSC conventions 'DET-FRAMETYPE-STARTTIME--DATALEN.txt', e.g.: 'H-H1_GWOSC_4_V1-1126259446-32.txt'. See https://www.gw-openscience.org for more infomation. This requirement can be relaxed by activating the 'ignore-data-filename' option.\n")
                assert not(fname==''), "Data are empty. Either pass valid data or select one of the 'download-data' or 'gaussian-noise' options."
                if not('.gwf' in fname):
                    ifo_name, fr_type, starttime, T = ((fname.split('/'))[-1]).strip('.txt').split('-')
                    rawstrain = np.loadtxt(fname)
                else:
                    ifo_name, fr_type, starttime, T = ((fname.split('/'))[-1]).strip('.gwf').split('-')
                    channel   = kwargs['channel-{}'.format(ifo)]
                    tseries   = TimeSeries.read(fname, channel)
                    rawstrain = np.array(tseries.data)
                starttime     = float(starttime)
                T             = float(T)
                dt            = T/len(rawstrain)
            else:
                # If the file name does not follow GWOSC conventions, times corresponding to the given strain must also be passed in the file (this could be made more general by passing custom {starttime, srate, T}, but this way is probably more stable).
                times, rawstrain = np.loadtxt(fname, unpack=True)
                starttime        = float(times[0])
                dt               = float(times[1] - times[0])
                T                = dt * len(rawstrain)
            srate_dt = 1./dt
            sys.stdout.write('\n* Loaded `{}` starting at `{}` length {}s.\n\n'.format(fname,starttime,T))
    else:
        # If no data file was passed either download them or generate them yourself.
        if(download_data_flag):
            T         = float(kwargs['datalen-download'])
            channel   = kwargs['channel-{}'.format(ifo)]
            starttime = np.int(triggertime)-(T/2.)
            endtime   = np.int(triggertime)+(T/2.)

            if((kwargs['gw-data-find']==1) and not(kwargs['gw-data-type-{}'.format(ifo)]=='')):
                connection = datafind.GWDataFindHTTPConnection()
                cache      = connection.find_frame_urls(ifo[0], kwargs['gw-data-type-{}'.format(ifo)], starttime, endtime, urltype='file')
                tseries    = TimeSeries.read(cache, channel)
            else:
                sys.stdout.write('\n* Using GWPY to download data.\n\n')
                tag        = kwargs['tag']
                tseries    = fetch_data(ifo, starttime, endtime, channel=channel, path=None, verbose=2, tag=tag)
            rawstrain               = np.array(tseries.data)
            dt                      = tseries.dt.to_value()
            srate_dt                = tseries.sample_rate.to_value()
            sys.stdout.write('\n* Loaded channel {} starting at {} length {}s.\n\n'.format(channel,starttime,T))
        elif(not(kwargs['gaussian-noise']=='')):

            # If requested by the user, fix the noise seed.
            if not(kwargs['gaussian-noise-seed']==-1):
                if(  ifo=='H1'): np.random.seed(kwargs['gaussian-noise-seed'])
                elif(ifo=='L1'): np.random.seed(kwargs['gaussian-noise-seed']+1)
                elif(ifo=='V1'): np.random.seed(kwargs['gaussian-noise-seed']+2)
                else: raise ValueError("Noise generation for this detector not supported. Please add the detector to the noise generation.")

            T            = int(kwargs['injection-T'])
            starttime    = triggertime - T/2.
            dt           = 1.0/srate
            srate_dt     = srate
            if not(kwargs['run-type']=='post-processing'):
                if(kwargs['gaussian-noise']=='white'):
                    sys.stdout.write('* Generating white gaussian noise with zero mean and sigma = {}.\n\n'.format(kwargs['gaussian-noise-white-sigma']))
                    rawstrain = np.random.normal(loc=0.0, scale=kwargs['gaussian-noise-white-sigma'], size=int(T*srate))
                elif('coloured' in kwargs['gaussian-noise']):
                    assert (signal_seglen==noise_seglen), "The injected psd is being interpolated on a frequency set determined by the noise seglen. A consistent signal seglen is required to obtain an unbiased estimation."
                    if not(kwargs['acf-{}'.format(ifo)]==''):
                        times_cgn, ACF_cgn  = kwargs['acf-{}'.format(ifo)]
                        C_cgn               = toeplitz(ACF_cgn)
                        cgn                 = multivariate_normal(mean = np.zeros(C_cgn.shape[0]), cov = C_cgn)
                        rawstrain           = cgn.rvs()
                    elif not(kwargs['psd-{}'.format(ifo)]==''):
                        psd_file            = kwargs['psd-{}'.format(ifo)]
                        sys.stdout.write('* Generating coloured gaussian noise with zero mean and PSD given by `{}`.\n\n'.format(psd_file))
                        freqs_file, psd_cgn = np.loadtxt(psd_file, unpack=True)
                        if('ASD' in psd_file):
                            print("* An ASD was passed, thus the ASD is being squared to compute the PSD.\n")
                            psd_cgn = psd_cgn*psd_cgn
                        N_points  = int(T*srate)
                        psd_cgn   = interp1d(freqs_file, psd_cgn, fill_value='extrapolate', bounds_error=False)
                        freqs_cgn = np.fft.rfftfreq(N_points, d = dt)
                        df_cgn    = np.diff(freqs_cgn)[0]
                        if(kwargs['gaussian-noise'] == 'coloured-TD'):
                            # FIXME: when chosen fixing a gaussian-noise-seed, it gives a MemoryError. To be tested.
                            review_warning()
                            sys.stdout.write('* Generating the noise in time domain.\n\n')
                            # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
                            ACF_cgn            = 0.5*np.real(np.fft.irfft(psd_cgn(freqs_cgn)*df_cgn))*N_points
                            C_cgn              = toeplitz(ACF_cgn)
                            cgn                = multivariate_normal(mean = np.zeros(C_cgn.shape[0]), cov = C_cgn)
                            rawstrain          = cgn.rvs()
                        elif(kwargs['gaussian-noise'] == 'coloured-FD'):
                            sys.stdout.write('* Generating the noise in frequency domain.\n\n')
                            # Range in which LIGO-Virgo noise is under control. Exact values are unimportant, since the PSD will be estimated from the generated strain after bandpassing is potentially applied.
                            f_min_inj = np.max([11.0, freqs_cgn.min()])
                            f_max_inj = np.min([4096., freqs_cgn.max()])
                            kmin = np.int(f_min_inj/df_cgn)
                            kmax = np.int(f_max_inj/df_cgn)
                            frequencies      = df_cgn*np.arange(0,N_points/2.+1)
                            frequency_strain = np.zeros(len(frequencies), dtype = np.complex64)
                            for i in range(kmin, kmax+1):
                                sigma_cgn = 0.5*np.sqrt(psd_cgn(frequencies[i])/df_cgn)
                                frequency_strain[i] = np.random.normal(0.0,sigma_cgn)+1j*np.random.normal(0.0,sigma_cgn)
                            rawstrain = np.real(np.fft.irfft(frequency_strain))*df_cgn*N_points
                        else:
                            raise ValueError("* To generate gaussian noise, the allowed options are: 'white', 'coloured-TD', 'coloured-FD'.")
                    else:
                        raise Exception("* If coloured gaussian noise is selected, an ACF or PSD from which the noise should be generated must be passed in input.")
                else:
                    raise ValueError("* Unknown gaussian noise option selected.")
                np.savetxt(os.path.join(kwargs['output'],'Noise','rawstrain_gaussian_noise_{}_{:d}_{:d}_{:d}.txt'.format(ifo, int(starttime), int(T), int(srate))), rawstrain)
            else:
                sys.stdout.write('* Reading the strain previously generated with gaussian noise.\n\n')
                rawstrain = np.loadtxt(os.path.join(kwargs['output'],'Noise','rawstrain_gaussian_noise_{}_{:d}_{:d}_{:d}.txt'.format(ifo, int(starttime), int(T), int(srate))))
        else:
            raise Exception("* Either pass a data file, download data or generate data.")

    # Safety checks.
    check_seglen_compatibility(signal_chunk_size, noise_chunk_size, T)
    check_sampling_rate_compatibility(srate, srate_dt)


    ##############################
    # Data conditioning section. #
    ##############################

    rawstrain, starttime, T = excise_nans_from_strain(rawstrain, starttime, T, triggertime, signal_chunk_size, dt, ifo_datafile, download_data_flag)
    strain                  = bandpass_data(rawstrain, f_min_bp, f_max_bp, srate_dt, bandpassing_flag)
    strain, dt              = downsample_data(strain, srate, srate_dt)


    ########################################################
    # Time axis and on-source strain construction section. #
    ########################################################

    # Construct the time axis and compute the index of the trigtime (i.e. the estimate of the coalescence time of a signal or the time at which the injection should be placed). Then compute the closest datapoint to the requested trigtime, this is the true time sample corresponding to the trigtime on our discretised axis. This adds a maximum shift to the requested starttime of `0.5*dt`.
    times            = np.linspace(starttime, starttime+T-dt, len(strain))
    index_trigtime   = round((triggertime-starttime)*srate)
    triggertime_data = times[index_trigtime]

    # Find the on-source chunk, centered on the trigger time, and the off-source chunk to avoid including the signal in the PSD computation.
    # Since the ACF might be computed on a windowed chunk through an fft, the onsource chunk must be windowed when no truncation is applied and the fft requested, to avoid normalisation inconsistencies.
    on_source_strain, off_source_strain = compute_on_off_source_strain(strain, signal_seglen, index_trigtime)
    on_source_strain                    = window_onsource_strain(on_source_strain, signal_seglen, noise_seglen, window_onsource_flag, window_flag, alpha_window, truncate)


    ###############################
    # ACF/PSD estimation section. #
    ###############################

    psd_window                       = tukey(noise_seglen, alpha_window)
    psd_window_norm                  = np.sum(psd_window**2)/noise_seglen
    psd_welch, freqs_welch, df_welch = compute_Welch_PSD(off_source_strain, srate, noise_seglen, psd_window)

    ACF, whitening_PSD = compute_acf_and_whitening_psd(times, strain, starttime, T, srate, triggertime, index_trigtime, dt, window_flag, alpha_window, noise_chunk_size, noise_seglen, signal_seglen, f_min_bp, f_max_bp, fft_acf, freqs_welch, psd_welch, ifo, kwargs)


    ###################################
    # Covariance computation section. #
    ###################################

    # Restrict the ACF on the signal chunk and produce the covariance matrix from the ACF.
    if(truncate):
        ACF_signal = ACF[:kwargs['analysis-duration-n']]
        np.savetxt(kwargs['output']+'/Noise/ACF_TD_cropped_{}_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate, kwargs['analysis-duration']), ACF_signal)
    else:
        ACF_signal = ACF[:signal_seglen]
    Covariance_matrix_signal = toeplitz(ACF_signal)


    ########################
    # ACF testing section. #
    ########################

    string_output = 'ifo_{}_starttime_{}_duration_{}_seglen_{}_srate_{}.txt'.format(ifo, int(starttime), int(T), kwargs['analysis-duration'], srate)

    check_Plancherel_ratio(psd_window_norm, df_welch, psd_welch, dt, ACF, debug)
    check_covariance_matrix_inversion_stability(Covariance_matrix_signal, debug)
    check_data_gaussianity(times, strain, Covariance_matrix_signal, signal_seglen, triggertime, string_output, kwargs['output'])
    chisquare_computation(ACF, chisquare_flag)


    ######################
    # Injection section. #
    ######################

    if not(kwargs['injection-approximant']==''):
        on_source_strain = add_injection(on_source_strain, strain, starttime, T, ifo, triggertime, index_trigtime, signal_seglen, kwargs)
    else:
        assert not((ifo_datafile=='') and not(download_data_flag)), "No data was passed and no injection has been selected. Exiting."


    ####################
    # Finalise output. #
    ####################

    # We are done with the strain.
    del rawstrain, strain

    # Return the time series, the covariance matrix and the PSD used in the whitened waveform plot.
    # Note that the `on_source_strain` is long `signal_seglen` and has not been truncate yet, unlike the ACF, to allow for a variable start time.
    return on_source_strain, ACF_signal, Covariance_matrix_signal, whitening_PSD



########################
# Main detector class. #
########################

class detector:

    def __init__(self, ifo_name, datafile, **kwargs):
        self.name                                             = ifo_name
        self.lal_detector                                     = lal.cached_detector_by_prefix[self.name]
        self.location                                         = self.lal_detector.location
        self.time_series, self.acf, self.covariance, self.psd = load_data(self.name, datafile, **kwargs)
        time_axis_internal                                    = np.linspace(-kwargs['signal-chunksize']/2, kwargs['signal-chunksize']/2, len(self.time_series)+1)[:-1]
        self.time                                             = kwargs['trigtime'] + time_axis_internal # technically the correct time axis should be centered around the closest datapoint to 'trigtime', i.e. time[index_trigtime], which is slightly different. However in practise this doesn't matter (except for plotting purposes) since in the likelihood 'trigtime' is going to be subtracted again. In other words, the index around which the time_series is centered is the true triggertime used in the likelihood computation.
        
        # Save the times and data that will be actually used in the likelihood.
        np.savetxt(kwargs['output']+'/Noise/signal_chunk_times_data_{det}.txt'.format(det=ifo_name), np.column_stack((self.time, self.time_series)))

        self.inverse_covariance = inv(self.covariance)
        self.cholesky           = np.linalg.cholesky(self.covariance)

        if kwargs['no-lognorm']: self.log_normalisation = 0.
        else:                    self.log_normalisation = -0.5*toeplitz_slogdet(self.covariance[0])[1] - 0.5*(self.covariance.shape[0])*np.log(2.0*np.pi)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lal_detector']
        del state['location']
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.lal_detector = lal.cached_detector_by_prefix[self.name]
        self.location = self.lal_detector.location



##################################################
# {Old/currently unused/work in progress} stuff. #
##################################################

def mem_psd(freqs_LAL, dt, data, M_max):

    review_warning()

    return mem.psd(freqs_LAL, dt, data, M_max)

def compute_maxent_PSD(times, strain, starttime, T, srate, triggertime, index_trigtime, dt, alpha_window, noise_seglen, signal_seglen, fft_acf, freqs_welch, psd_welch, ifo, kwargs):

    # References: https://arxiv.org/abs/2106.09499
    review_warning()
    assert (fft_acf), "Cannot compute ACF in time domain and compute MaxEnt PSD."
    freqs_default = np.fft.rfftfreq(noise_seglen, d = dt)
    df_default    = np.diff(freqs_default)[0]
    if(kwargs['maxent-psd']=='average'):
        sys.stdout.write('* Computing the one-sided average PSD with the MESA method.\n\n')
        M_max       = int(2.*noise_seglen/np.log(2.*noise_seglen))
        psds        = [mem_psd(freqs_default, dt, data, M_max) for data in chunks_iterator(times, strain, noise_seglen, avoid=triggertime, window=window_flag, alpha=alpha_window)]

        if(  kwargs['noise-averaging-method']=='mean'  ): psd_maxent = np.mean(  np.array(psds), axis=0)
        elif(kwargs['noise-averaging-method']=='median'): psd_maxent = np.median(np.array(psds), axis=0)

        ACF = 0.5*np.real(np.fft.irfft(psd_maxent*df_default))*noise_seglen
    else:
        M_max = int(2.*signal_seglen/np.log(2.*signal_seglen))
        if(kwargs['maxent-psd']=='onsource-chunk'):
            sys.stdout.write('* Computing the one-sided PSD with the MESA method on the onsource chunk.\n\n')
            if not((signal_seglen%2)==0): data = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2+1]
            else                        : data = strain[index_trigtime-signal_seglen//2:index_trigtime+signal_seglen//2]
        elif(kwargs['maxent-psd']=='pre-onsource-chunk'):
            sys.stdout.write('* Computing the one-sided PSD with the MESA method on the pre-onsource chunk.\n\n')
            if not((signal_seglen%2)==0): data = strain[index_trigtime-signal_seglen//2-signal_seglen:index_trigtime-signal_seglen//2+1]
            else                        : data = strain[index_trigtime-signal_seglen//2-signal_seglen:index_trigtime-signal_seglen//2]
        elif(kwargs['maxent-psd']=='post-onsource-chunk'):
            sys.stdout.write('* Computing the one-sided PSD with the MESA method on the post-onsource chunk.\n\n')
            if not((signal_seglen%2)==0): data = strain[index_trigtime+signal_seglen//2:index_trigtime+signal_seglen//2+1+signal_seglen]
            else                        : data = strain[index_trigtime+signal_seglen//2:index_trigtime+signal_seglen//2+signal_seglen]
        psd_maxent = mem_psd(freqs_default, dt, data, M_max)
        # We are using the one-sided PSD, thus it is twice the Fourier transform of the autocorrelation function (see eq. 7.15 of Maggiore Vol.1). We take the real part just to convert the complex output of fft to a real numpy float. The imaginary part if already 0 when coming out of the fft.
        ACF = 0.5*np.real(np.fft.irfft(psd_maxent*df_default))*signal_seglen

    plots.plot_ACF(time        = dt*np.arange(len(ACF)),
                   acf         = ACF,
                   label       = '$\mathrm{ACF \,\, from \,\, MaxEnt}$',
                   output_path = os.path.join(kwargs['output']+'/Noise','{}_ACF.pdf'.format(ifo)))
    plots.plot_PSD_compare(freqs1      = freqs_default,
                           psd1        = psd_maxent,
                           label1      = "$\mathrm{PSD \,\, from \,\, MaxEnt}$",
                           freqs2      = freqs_welch,
                           psd2        = psd_welch,
                           label2      = "$\mathrm{Welch, \,\, frequency \,\, domain}$",
                           output_path = os.path.join(kwargs['output'],'Noise','{}_PSD.pdf'.format(ifo)))

    np.savetxt(os.path.join(kwargs['output'],'Noise','ACF_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((dt*np.arange(len(ACF)), ACF)))
    np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_MaxEnt_{}_{}_{}_{}_{}_{}.txt'.format(kwargs['maxent-psd'], ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_default, psd_maxent)))
    np.savetxt(os.path.join(kwargs['output'],'Noise','PSD_Welch_{}_{}_{}_{}_{}.txt'.format(ifo, int(starttime), int(T), noise_chunk_size, srate)), np.column_stack((freqs_welch, psd_welch)))
    whitening_PSD = psd_maxent

    return ACF, whitening_PSD

def non_stationarity_check(acfs, dt):

    review_warning()
    #Check if there is any trend in PSD evolution.
    # color = iter(cm.viridis(np.linspace(0,1,len(acfs))))
    #FIXME(optional): tolerance needs to be tested. Stochastic group plenary talk LVC Sept 2019 used tolerance=0.2
    plt.figure()
    counter = 0
    #FIXME(optional): random value, test it
    tolerance = 4.0
    sys.stdout.write('* Non-stationarity check (%f maximum tolerated variation)\n\n'%tolerance)
    for idx in range(len(acfs)):
        psd_x   = 2*np.real(np.fft.rfft(acfs[idx]*dt))
        if not(idx==0 or idx==(len(acfs)-1)):
            psd_pre  = 2*np.real(np.fft.rfft(acfs[idx-1]*dt))
            psd_post = 2*np.real(np.fft.rfft(acfs[idx+1]*dt))
            for x in range(0, len(psd_x)):
                statistic = np.abs(psd_x[x] - ((psd_post[x] + psd_pre[x])/2.))/psd_x[x]
                if(statistic > tolerance): counter = counter + 1
            sys.stdout.write('Number of non-stationary bins in chunk %d: %d/%d.\n\n'%(idx, counter, len(freqs_default)))
            counter          = 0
#        c = next(color)
#        plt.loglog(freqs2, psd_x, lw=0.1, alpha=0.5, c=c)
#    plt.xlabel(r"$f\,(Hz)$",        fontsize=18)
#    plt.ylabel(r"$S(f)\,(Hz^{-1})$",fontsize=18)
#    plt.legend()
#    plt.savefig(os.path.join(kwargs['output'],'Noise','{}_PSD_variation.pdf'.format(ifo)), bbox_inches='tight')
#            plt.close('all')

    return

def UNCHECKED_acf_from_ideal_psd(ASDtxtfile, fmin, srate, T):

    review_warning()
    def interpolate_psd(psd_in, f_in, df_out, fmin, srate):
        f_out = np.arange(fmin, srate/2., df_out)
        return f_out, np.interp(f_out, f_in, psd_in)

    # Read PSD from file
    f, asd  = np.loadtxt(ASDtxtfile, unpack = True)
    dt      = 1./srate
    psd     = asd**2

    # Interpolate PSD on a chosen set of frequencies
    fo, psd = interpolate_psd(psd, f, 1./T, f.min(), srate)

    # Build the ACF
    R   = np.fft.irfft(psd)*srate
    lag = np.linspace(0,T/2.,len(R))

    return lag, R

def UNCHECKED_estimated_acf(x):
    
    review_warning()
    n = len(x)
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    
    return r/np.arange(n, 0, -1)

def UNCHECKED_acf_finite(y,k):

  """
  Estimate directly from the data y
  Weighting by 1/(N-i) for lag i where N=len(y)
  k specifies the desired size of the ACF,
  i.e. the number of samples in the on-source segment
  """

  review_warning()
  N = len(y)
  R = [sum(y[:N-i]*y[i:N])/(N-i) for i in range(k)]

  return R
