from pathlib import Path

## ~~ SAVE SPEED AS TXT USING SPECIAL __FILE__ VARIABLE ~~ ##

def save_speed_as_txt(speed, file_path):
    estimate_kmps_formatted = "{:.4f}".format(speed)
    base_folder = Path(__file__).parent.resolve()
    data_file = base_folder / "result.txt"
    for i in range(10):
        with open(data_file, "w", buffering=1) as f:
            f.write(f"{estimate_kmps_formatted}")
