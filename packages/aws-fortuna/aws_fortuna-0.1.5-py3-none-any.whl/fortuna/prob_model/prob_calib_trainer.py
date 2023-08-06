from fortuna.calibration.calibrator import CalibTrainerABC
from fortuna.calibration.calib_state import CalibState
from typing import Callable, Any, Union, Tuple, Optional, Dict
import jax.numpy as jnp
from flax.core import FrozenDict
from fortuna.typing import CalibMutable, CalibParams, Batch, Array
from optax._src.base import PyTree
from jax._src.prng import PRNGKeyArray


class ProbCalibTrainer(CalibTrainerABC):
    def training_loss_step(
        self,
        fun: Callable[[Any], Union[float, Tuple[float, dict]]],
        params: CalibParams,
        batch: Batch,
        mutable: CalibMutable,
        rng: PRNGKeyArray,
        n_data: int,
    ) -> Tuple[jnp.ndarray, Dict[str, Any]]:
        return_aux = ["outputs"]
        if mutable is not None:
            return_aux += ["mutable"]
        loss, aux = fun(
            batch,
            n_data=n_data,
            return_aux=["outputs", "calib_mutable"],
            ensemble_outputs=self.outputs,
            calib_params=params,
            calib_mutable=mutable,
            rng=rng,
        )
        loss = -loss
        logging_kwargs = None
        return (
            loss,
            {
                "outputs": aux.get("outputs"),
                "mutable": aux.get("mutable"),
                "logging_kwargs": logging_kwargs,
            },
        )

    def validation_step(
        self,
        state: CalibState,
        batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, jnp.ndarray, Array], float], ...]] = None,
        unravel: Optional[Callable[[any], PyTree]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Dict[str, jnp.ndarray]:
        log_probs, aux = fun(
            batch,
            n_data=n_data,
            return_aux=["outputs"],
            ensemble_outputs=self.outputs,
            calib_params=state.params,
            calib_mutable=state.mutable,
            rng=rng,
        )

        if metrics is not None:
            val_metrics = self.compute_metrics(
                self.predict_fn(aux["outputs"]), self.uncertainty_fn(aux["outputs"]), batch[1], metrics
            )
            return {
                "val_loss": -log_probs,
                **{f"val_{m}": v for m, v in val_metrics.items()},
            }
        return dict(val_loss=-log_probs)

    def __str__(self):
        return "calibration"


class JittedProbCalibTrainer(JittedMixin, ProbCalibTrainer):
    pass


class MultiGPUMAPTrainer(MultiGPUMixin, ProbCalibTrainer):
    pass
