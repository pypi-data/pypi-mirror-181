import matplotlib.pyplot as plt
from astropy.table import QTable
import numpy as np
import astropy.units as u
from pyirf.binning import create_bins_per_decade, add_overflow_bins, bin_center
from astropy.io import fits
from astropy.visualization import quantity_support
from ctaplot import ana
import sklearn
from sklearn.multiclass import LabelBinarizer
from matplotlib import ticker


DEFAULT_ENERGY_UNIT = u.TeV
DEFAULT_ENERGY_BINS = create_bins_per_decade(e_min=10 * u.GeV, e_max=100 * u.TeV, bins_per_decade=5)
DEFAULT_THETA2_BINS = np.linspace(0*u.deg**2, 0.4*u.deg**2, num=81)

def format_yaxis_degrees(ax):
    # issue with degrees label formatting see https://github.com/astropy/astropy/issues/13211
    fmt = '{x:.2f}°' if abs(ax.get_ylim()[1] - ax.get_ylim()[0]) < 1 else '{x:.1f}°'
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter(fmt))
    return ax


class Metric:
    name = 'metric'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_file(cls, filename):
        table = QTable.read(filename, hdu=cls.name)
        return cls(table['x'], table['y'], table[cls.name])

    def write(self, filename, overwrite=False, append=False):
        """
        Write the metric to a FITS file.

        Parameters
        ----------
        filename: Path | str
            Path to the file to write with the extension .fits.
        overwrite: bool
            If True, overwrite the file if it exists.
        append: bool
            If True, append to the file if it exists, or create it if not.
        """
        hdu = fits.BinTableHDU(self.table, name=self.name)

        if append:
            with fits.open(filename, mode='append') as hdulist:
                hdulist.append(hdu)
        else:
            hdus = [
                fits.PrimaryHDU(),
                hdu
            ]
            fits.HDUList(hdus).writeto(filename, overwrite=overwrite)

    @classmethod
    def from_events(cls, true, reco, x):
        raise NotImplementedError("Should be implemented in child class")

    def plot(self, ax=None, **kwargs):
        ax = plt.gca() if ax is None else ax
        ax.plot(self.x, self.y, **kwargs)
        return ax

    @property
    def table(self):
        return QTable({
            'x': self.x,
            'y': self.y,
        })

class MetricPerBin(Metric):
    name = 'metric'

    def __init__(self, x_low, x_high, y):
        self.x_low = x_low
        self.x_high = x_high
        self.y = y

    @classmethod
    def from_events(cls, true, reco, x, x_bins=10):
        raise NotImplementedError("Should be implemented in child class")

    def table(self):
        return QTable({
            'x_low': self.x_low,
            'x_high': self.x_high,
            'y': self.y,
        })

    @classmethod
    def from_file(cls, filename):
        table = QTable.read(filename, hdu=cls.name)
        return cls(table['x_low'], table['x_high'], table[cls.name])


class MetricPerEnergyBin(Metric):
    name = 'metric_per_energy'

    def __init__(self, energy_bins, metric):
        self._energy_bins = energy_bins.to(DEFAULT_ENERGY_UNIT)
        self._metric = metric

    @property
    def energy_bins(self):
        return self._energy_bins

    @property
    def energy_low(self):
        return self.energy_bins[:-1]

    @property
    def energy_high(self):
        return self.energy_bins[1:]

    @property
    def table(self):
        return QTable({
            'energy_low': self.energy_low,
            'energy_high': self.energy_high,
            self.name: self._metric,
        })

    @property
    def energy_center(self):
        return bin_center(self.energy_bins)

    @classmethod
    def from_file(cls, filename):
        table = QTable.read(filename, hdu=cls.name)
        return cls(table['energy_low'], table['energy_high'], table[cls.name])

    @classmethod
    def from_events(cls, true, reco, energy, energy_bins=DEFAULT_ENERGY_BINS):
        raise NotImplementedError("Should be implemented in child class")

    def plot(self, ax=None, **kwargs):
        ax = plt.gca() if ax is None else ax

        kwargs.setdefault('label', self.name)
        with quantity_support():
            ax.errorbar(self.energy_center,
                        self._metric,
                        xerr=[self.energy_center - self.energy_low, self.energy_high - self.energy_center],
                        **kwargs,
                        )
        ax.set_xscale('log')
        ax.set_xlabel(f'Energy / {self.energy_center.unit}')
        ax.set_title(self.name)
        return ax


class ResolutionPerEnergyBin(MetricPerEnergyBin):
    name = 'resolution'

    def __init__(self, energy_bins, resolution):
        super().__init__(energy_bins, resolution)

    @classmethod
    def from_events(cls, true, reco, energy, energy_bins=DEFAULT_ENERGY_BINS):
        _, res = ana.resolution_per_energy(true, reco, energy, bins=energy_bins)
        return cls(energy_bins, res[:,0])


class AngularResolutionPerEnergyBin(MetricPerEnergyBin):
    name = 'angular_resolution'

    def __init__(self, energy_bins, angular_resolution):
        super().__init__(energy_bins, angular_resolution)

    @classmethod
    def from_events(cls, true_alt, reco_alt, true_az, reco_az, true_energy, energy_bins=DEFAULT_ENERGY_BINS):
        _, res = ana.angular_resolution_per_energy(true_alt, reco_alt, true_az, reco_az, true_energy, bins=energy_bins)
        return cls(energy_bins, res[:,0])

    def plot(self, ax=None, **kwargs):
        ax = super().plot(ax=ax, **kwargs)
        format_yaxis_degrees(ax)
        return ax


class EnergyResolutionPerEnergyBin(MetricPerEnergyBin):
    name = 'energy_resolution'

    def __init__(self, energy_bins, energy_resolution):
        super().__init__(energy_bins, energy_resolution)


    @classmethod
    def from_events(cls, true_energy, reco_energy, energy_bins=DEFAULT_ENERGY_BINS):
        _, res = ana.energy_resolution_per_energy(true_energy, reco_energy, bins=energy_bins)
        return cls(energy_bins, res[:,0])


class ImpactResolutionPerEnergyBin(MetricPerEnergyBin):
        name = 'impact_resolution'

        def __init__(self, energy_bins, impact_resolution):
            super().__init__(energy_bins, impact_resolution)

        @classmethod
        def from_events(cls, true_alt, reco_alt, true_az, reco_az, true_energy, energy_bins=DEFAULT_ENERGY_BINS):
            _, res = ana.impact_resolution_per_energy(true_x, reco_x, true_y, reco_y, true_energy, bins=energy_bins)
            return cls(energy_bins, res[:,0])


class ROCCurve(Metric):
    name = 'roc'

    def __init__(self, fpr, tpr):
        """

        Parameters
        ----------
        fpr: array
            false positive rate
        tpr: array
            true positive rate
        """
        self.tpr = tpr
        self.fpr = fpr

    @classmethod
    def from_events(cls, true_type, reco_proba, pos_label=None, sample_weight=None, drop_intermediate=True):
        auc_score = sklearn.metrics.roc_auc_score(true_type, reco_proba)
        if auc_score < 0.5:
            auc_score = 1 - auc_score

        fpr, tpr, thresholds = sklearn.metrics.roc_curve(true_type,
                                                         reco_proba,
                                                         pos_label=pos_label,
                                                         sample_weight=sample_weight,
                                                         drop_intermediate=drop_intermediate,
                                                         )
        return cls(fpr, tpr)

    @property
    def table(self):
        return QTable({
            'fpr': self.fpr,
            'tpr': self.tpr,
        })


    def plot(self, ax=None, **kwargs):
        ax = plt.gca() if ax is None else ax
        roc_auc = sklearn.metrics.auc(self.fpr, self.tpr)
        rcd = sklearn.metrics.RocCurveDisplay(fpr=self.fpr, tpr=self.tpr, roc_auc=roc_auc)
        rcd.plot(ax=ax, **kwargs)
        return ax

    @classmethod
    def from_file(cls, filename):
        table = QTable.read(filename, hdu=cls.name)
        return cls(table['fpr'], table['tpr'])


class ROCCurveGamma(ROCCurve):
    name = 'roc_gamma'
    def __init__(self, fpr, tpr):
        super().__init__(fpr, tpr)

    def plot(self, ax=None, **kwargs):
        ax = super().plot(ax=ax, **kwargs)
        ax.set_xlabel('')
        ax.set_title("gamma ROC curve")
        ax.set_xlabel("gamma false positive rate")
        ax.set_ylabel("gamma true positive rate")
        return ax

    @classmethod
    def from_events(cls, true_type, gammaness,
                    gamma_label=0,
                    sample_weight=None,
                    drop_intermediate=True):

        from sklearn.preprocessing import label_binarize
        from sklearn.multiclass import OneVsRestClassifier

        if gamma_label is not None and gamma_label in set(true_type):
            label_binarizer = LabelBinarizer()
            binarized_classes = label_binarizer.fit_transform(true_type)

            ii = np.argwhere(label_binarizer.classes_ == gamma_label)[0][0]

            return super().from_events(binarized_classes[:, ii],
                                        gammaness,
                                        pos_label=1,
                                        sample_weight=sample_weight,
                                        drop_intermediate=drop_intermediate)


        else:
            raise ValueError(f"true_type must contain gamma_label {gamma_label}")

    def plot(self, ax=None, **kwargs):
        return super().plot(ax=ax, **kwargs)


class EnergyBias(MetricPerEnergyBin):
    name = 'energy_bias'

    def __init__(self, energy_bins, energy_bias):
        super().__init__(energy_bins, energy_bias)

    @classmethod
    def from_events(cls, true_energy, reco_energy, energy_bins=DEFAULT_ENERGY_BINS):
        _, res = ana.energy_bias_per_energy(true_energy, reco_energy, bins=energy_bins)
        return cls(energy_bins, res[:,0])


class Theta2(Metric):
    name = 'theta2'

    def __init__(self, theta2_bins, theta2_values):
        self.theta2_bins = theta2_bins
        self.theta2_values = theta2_values

    @property
    def theta2_low(self):
        return self.theta2_bins[:-1]

    @property
    def theta2_high(self):
        return self.theta2_bins[1:]

    @classmethod
    def from_events(cls, true_alt, reco_alt, true_az, reco_az, bias_correction=False, bins=DEFAULT_THETA2_BINS):
        from ctaplot.ana.ana import theta2
        ang_sep = theta2(true_alt, reco_alt, true_az, reco_az, bias_correction=bias_correction)
        theta2_values, theta2_bins = np.histogram(ang_sep, bins=bins)
        return cls(theta2_bins=theta2_bins, theta2_values=theta2_values)

    @property
    def table(self):
        return QTable({
            'theta2_low': self.theta2_low,
            'theta2_high': self.theta2_high,
            'theta2_values': self.theta2_values,
        })

    def plot(self, ax=None, **kwargs):
        ax = plt.gca() if ax is None else ax
        with quantity_support():
            ax.stairs(self.theta2_values, edges=self.theta2_bins.to(u.deg**2), **kwargs)
        ax.set_xlabel(r'angular separation ($deg^2$)')
        ax.set_ylabel('count')
        return ax

    @classmethod
    def from_file(cls, filename):
        table = QTable.read(filename, hdu=cls.name)
        theta2_bins = np.append(table['theta2_low'], table['theta2_high'][-1])
        return cls(theta2_bins, table['theta2_values'])


def angular_separation_bias(true_alt, reco_alt, true_az, reco_az):
    from astropy.coordinates import angular_separation
    ang_sep = angular_separation(true_az.mean(), reco_az.mean(), true_alt.mean(), reco_alt.mean())
    return ang_sep

def angular_separation_bias_per_energy(true_alt, reco_alt, true_az, reco_az, true_energy, energy_bins=DEFAULT_ENERGY_BINS):
    biases = []
    for i in range(len(energy_bins) - 1):
        low = energy_bins[i]
        high = energy_bins[i+1]
        mask = (true_energy >= low) & (true_energy < high)
        biases.append(angular_separation_bias(true_az[mask], true_alt[mask], reco_az[mask], reco_alt[mask]))
    return energy_bins, u.Quantity(biases)


class AngularSeparationBiasPerEnergy(MetricPerEnergyBin):
    name = 'angular_separation_bias'

    def __init__(self, energy_low, energy_high, angular_separation_bias):
        super().__init__(energy_low, energy_high, angular_separation_bias.to(u.deg))

    @classmethod
    @u.quantity_input(true_alt=u.rad, reco_alt=u.rad, true_az=u.rad, reco_az=u.rad, true_energy=u.TeV, energy_bins=u.TeV)
    def from_events(cls, true_alt, reco_alt, true_az, reco_az, true_energy, energy_bins=DEFAULT_ENERGY_BINS):
        _, bias = angular_separation_bias_per_energy(true_alt, reco_alt, true_az, reco_az, true_energy, energy_bins=energy_bins)
        return cls(energy_bins[:-1], energy_bins[1:], bias)


    def plot(self, ax=None, **kwargs):
        ax = super().plot(ax=ax, **kwargs)
        ax.set_xlabel(f'Energy / {DEFAULT_ENERGY_UNIT}')
        ax.set_ylabel('angular separation bias')
        ax.set_xscale('log')
        format_yaxis_degrees(ax)
        return ax


class EffectiveArea(MetricPerEnergyBin):
    name = 'effective_area'

    def __init__(self, energy_bins, effective_area):
        super().__init__(energy_bins, effective_area)

    @classmethod
    def from_events(cls, gammas, simulation_info, energy_bins=DEFAULT_ENERGY_BINS):
        from pyirf.irf.effective_area import effective_area_per_energy
        effarea = effective_area_per_energy(gammas, simulation_info, energy_bins)
        return cls(energy_bins, effarea)

    def plot(self, ax=None, **kwargs):
        ax = super().plot(ax=ax, **kwargs)
        ax.set_ylabel(f'Effective area / {self._metric.unit}')
        ax.set_yscale('log')
        ax.grid(True, which='both')
        ax.set_axisbelow(True)
        return ax


class SkyMap(Metric):
    name = 'sky_map'

    def __init__(self, sky_map):
        self.sky_map = sky_map