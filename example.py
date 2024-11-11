import os
import pandas as pd
from utilities.lcz_utils import (
    convert_LCZ_num_to_class,
    load_LCZ_class_palette,
    get_LCZ_order,
)
from utilities.plot_utils import plot_pred_vs_actual

# ---> Data
data = pd.DataFrame(
    {
        "y_actual": [284, 287, 291, 295, 298, 302, 304, 310],
        "y_pred": [285, 286, 290, 296, 300, 304, 305, 308],
        "LCZ": [100100, 100123, 110200, 100123, 100456, 100456, 110700, 110200],
    }
)

# ---> Convert LCZ numerical codes to classes and get a QGIS-specific LCZ palette

# Absolute path to the directory of the current script
curr_dir = os.path.dirname(os.path.abspath(__file__))

# Map LCZmajority numerical codes in the predicted DataFrame into classes
data["LCZ"] = convert_LCZ_num_to_class(
    data["LCZ"],
    mapper_file_path=os.path.join(curr_dir, "assets/json/LCZ_num_to_class.json"),
)
# Get color palette for the LCZ classes
LCZ_class_to_palette = load_LCZ_class_palette(
    mapper_file_path=os.path.join(curr_dir, "assets/json/LCZ_class_to_palette.json"),
)

# Define list of unique LCZ classes in the predicted DataFrame ordered as in the map
hue_order = get_LCZ_order(
    data["LCZ"],
    LCZ_kind="class",
    mapper_file_path=os.path.join(curr_dir, "assets/json/LCZ_num_to_class.json"),
)

# ---> Plot
plot_pred_vs_actual(
    df=data,
    col_actual="y_actual",
    col_pred="y_pred",
    col_hue="LCZ",
    hue_title_fancy=r"$\mathrm{LCZ-Majority}$",
    hue_order=hue_order,
    hue_palette=LCZ_class_to_palette,
    # target_title_fancy=r"$\mathrm{LST}$",
    # target_units_title_fancy=r"$\mathrm{K}$",
    scores={r"$R^2$": 0.832, r"$\mathrm{RMSE}$": 0.873},
    use_hue=True,
    print_scores=True,
)
