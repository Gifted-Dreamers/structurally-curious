#!/bin/bash
# Session 51 Experiment Runner
# Waits for F3b to complete, then runs F11, F3c, F12 sequentially

MODEL="Qwen/Qwen2.5-7B-Instruct"
LOG_DIR="$HOME/experiments"

echo "=== Session 51 Experiment Queue ==="
echo "Started: $(date -u)"
echo "Waiting for F3b (PID 5525) to complete..."

# Wait for F3b
while kill -0 5525 2>/dev/null; do
    echo "  F3b still running... $(date -u '+%H:%M:%S')"
    sleep 300
done
echo "F3b completed: $(date -u)"
echo ""

# Activate environment
source ~/experiments-env/bin/activate
export OMP_NUM_THREADS=16
export TORCH_NUM_THREADS=16

# F11: Construction Load Gradient (~30 questions x ~140s = ~70 min)
echo "=== Starting F11: Construction Load Gradient ==="
echo "Start: $(date -u)"
mkdir -p ~/experiments/f11-results
python3 ~/f11_construction_load.py "$MODEL" ~/experiments/f11-results > $LOG_DIR/f11_qwen7b.log 2>&1
echo "F11 completed: $(date -u)"
echo ""

# F3c: Vocabulary on Failures (~20 questions x 2 conditions x ~140s = ~93 min)
echo "=== Starting F3c: Vocabulary on Failures ==="
echo "Start: $(date -u)"
mkdir -p ~/experiments/f3c-results
python3 ~/f3c_vocabulary_on_failures.py "$MODEL" ~/experiments/f3c-results > $LOG_DIR/f3c_qwen7b.log 2>&1
echo "F3c completed: $(date -u)"
echo ""

# F12: Scaffold Reconstruction (~10 questions x 2 phrasings x 3 conditions x ~140s = ~140 min)
echo "=== Starting F12: Scaffold Reconstruction ==="
echo "Start: $(date -u)"
mkdir -p ~/experiments/f12-results
python3 ~/f12_scaffold_reconstruction.py "$MODEL" ~/experiments/f12-results > $LOG_DIR/f12_qwen7b.log 2>&1
echo "F12 completed: $(date -u)"
echo ""

echo "=== All Session 51 experiments complete ==="
echo "Finished: $(date -u)"
echo "Total runtime: F3b + F11 (~70m) + F3c (~93m) + F12 (~140m) = ~5 hours after F3b"
