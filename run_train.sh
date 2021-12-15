#!/bin/bash

clear
export DEVICE=gpu

if [[ $DEVICE == cpu ]]
then
   export CUDA_VISIBLE_DEVICES="-1";
else
    export CUDA_VISIBLE_DEVICES="0";
fi

export OUT_DIR="output_$(date +"%m.%d.%H.%M")"

export SEED_LIST=(5 12 42)
export NUM_TRAIN_LIST=(32 64 100 200 500 1000)
export STEPS_LIST=(100 200)
export SEQ_LEN=128
export MODEL=bert-base-uncased
export LR=1e-05
export BS=4


for NUM_TRAIN in "${NUM_TRAIN_LIST[@]}"
do
    for SEED in "${SEED_LIST[@]}"
    do
        for STEPS in "${STEPS_LIST[@]}"
        do
            python3 cli.py \
                --method pet \
                --pattern_ids 1 \
                --data_dir sst \
                --model_type bert \
                --model_name_or_path $MODEL \
                --task_name yelp-polarity \
                --output_dir $OUT_DIR/"num_ex_$NUM_TRAIN"/"p1"/"$STEPS""_steps"/"seed_$SEED" \
                --eval_set "dev" \
                --train_examples $NUM_TRAIN \
                --pet_max_steps $STEPS \
                --pet_max_seq_length $SEQ_LEN \
                --pet_repetitions 1 \
                --do_train \
                --do_eval \
                --no_distillation \
                --learning_rate $LR \
                --pet_per_gpu_train_batch_size $BS \
                --seed $SEED \
                | tee ./$OUT_DIR/train.log
        done
    done
done

python aggregate.py $OUT_DIR