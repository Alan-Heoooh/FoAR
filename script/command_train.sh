torchrun --master_addr 192.168.1.1 --master_port 10000 --nproc_per_node 2 --nnodes 1 --node_rank 0 train.py --data_path /data/task --aug --aug_jitter --num_obs_force 200 --num_action 20 --num_action_force 300 --force_threshold 8 --voxel_size 0.005 --obs_feature_dim 512 --hidden_dim 512 --nheads 8 --num_encoder_layers 4 --num_decoder_layers 1 --dim_feedforward 2048 --dropout 0.1 --ckpt_dir /data/ckpt --batch_size 240 --num_epochs 1000 --save_epochs 100 --num_workers 50 --seed 233 
