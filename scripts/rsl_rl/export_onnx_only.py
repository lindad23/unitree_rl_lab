import argparse
import os
import torch

from rsl_rl.runners import OnPolicyRunner

# ----------------------------
# CLI
# ----------------------------
parser = argparse.ArgumentParser("Pure RSL-RL -> ONNX exporter (NO IsaacLab)")
parser.add_argument("--checkpoint", type=str, required=True)
parser.add_argument("--device", type=str, default="cpu")
args = parser.parse_args()

checkpoint_path = os.path.abspath(args.checkpoint)
export_dir = os.path.join(os.path.dirname(checkpoint_path), "exported")
os.makedirs(export_dir, exist_ok=True)

print(f"[INFO] Loading checkpoint: {checkpoint_path}")

# ----------------------------
# Load checkpoint FIRST (to get train_cfg)
# ----------------------------
ckpt = torch.load(checkpoint_path, map_location=args.device)

if "train_cfg" not in ckpt:
    raise RuntimeError(
        "Checkpoint does not contain 'train_cfg'. "
        "This script requires an RSL-RL training checkpoint."
    )

train_cfg = ckpt["train_cfg"]

# ----------------------------
# Create runner with REAL train_cfg
# ----------------------------
runner = OnPolicyRunner(
    None,          # env
    train_cfg,     # ✅ must contain 'algorithm'
    None,          # log_dir
    args.device,   # device
)

# ----------------------------
# Load weights
# ----------------------------
runner.load(checkpoint_path)

# ----------------------------
# Extract policy network
# ----------------------------
try:
    policy_nn = runner.alg.policy        # rsl-rl >= 2.3
except AttributeError:
    policy_nn = runner.alg.actor_critic  # rsl-rl <= 2.2

policy_nn.eval()
actor = policy_nn.actor

# ----------------------------
# Infer obs dim
# ----------------------------
# 假设 actor 是 nn.Sequential，第一层是 Linear
first_layer = actor[0]
obs_dim = first_layer.in_features
dummy_obs = torch.zeros(1, obs_dim, device=args.device)

# ----------------------------
# Export ONNX
# ----------------------------
onnx_path = os.path.join(export_dir, "policy.onnx")
print(f"[INFO] Exporting ONNX to {onnx_path}")

torch.onnx.export(
    actor,
    dummy_obs,
    onnx_path,
    input_names=["obs"],
    output_names=["action"],
    opset_version=17,
    do_constant_folding=True,
)

print("[SUCCESS] Pure ONNX export finished")
