import os
from collections import defaultdict
from pathlib import Path
from sys import argv

def main(out_dir: str) -> None:
    pattern_ids = [1]

    num_of_seeds = len(list(list((list(Path(out_dir).iterdir())[0]/f"p{pattern_ids[0]}").iterdir())[0].iterdir()))

    for pattern_id in pattern_ids:
        totals = {num_ex: defaultdict(int) for num_ex in os.listdir(out_dir)}
        time_totals = {num_ex: defaultdict(int) for num_ex in os.listdir(out_dir)}

        for root, dirs, files in os.walk(out_dir):
            if files and f"p{pattern_id}" in root:
                parts = Path(root).parts
                num_ex, steps = parts[1], parts[3].split('_')[0] 

                with open(Path(root) / 'result_test.txt') as f:
                    cur_acc = float(f.readline().split()[1])
                totals[num_ex][steps] += cur_acc

                for file in files:
                    if not file.startswith('result'):
                        time_totals[num_ex][steps] += float(file[:-1])

            for i in range(3):
                if f'p{i}-i0' in dirs:
                    dirs.remove(f'p{i}-i0')

        avg = defaultdict(dict)
        for num_ex, acc_per_steps in totals.items():
            num_ex = num_ex.split('_')[-1]
            for step, acc in acc_per_steps.items():
                avg[int(num_ex)][int(step)] = f"{(acc / num_of_seeds):.4f}"

        time_avg = defaultdict(dict)
        for num_ex, time_per_steps in time_totals.items():
            num_ex = num_ex.split('_')[-1]
            for step, time in time_per_steps.items():
                time_avg[int(num_ex)][int(step)] = f"{(time / num_of_seeds):.4f}"

        space = ' ' * 10
        print(f"\n\nPattern {pattern_id} - Average Accuracy\n")
        for i, num_ex in enumerate(sorted(avg.keys())):
            steps_list = sorted(avg[num_ex].keys())
            if i == 0:
                print(f'#ex\steps{space}' + f'{space}'.join(map(str, steps_list)))

            print(f"   {num_ex}{space}" + f'{space}'.join([avg[num_ex][steps] for steps in steps_list]))

        print(f"\n\nPattern {pattern_id} - Average Elapsed Time for Training (secs)\n")
        for i, num_ex in enumerate(sorted(time_avg.keys())):
            steps_list = sorted(time_avg[num_ex].keys())
            if i == 0:
                print(f'#ex\steps{space}' + f'{space}'.join(map(str, steps_list)))

            print(f"   {num_ex}{space}" + f'{space}'.join([time_avg[num_ex][steps] for steps in steps_list]))
        print('\n\n')


if __name__ == "__main__":
    main(argv[1])
