from scenario.tenTimesTen.experiment import run_experiment
from scenario.tenTimesTen.visualization import visualize

folder_generated = run_experiment()
visualize(folder_generated)
