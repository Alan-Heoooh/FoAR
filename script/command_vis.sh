python vis_point_cloud.py --ckpt /aidata/zihao_6024/ckpts/task_0207_cut/rise_1015/rise.ckpt --offset_ckpt /aidata/zihao_6024/ckpts/task_0701_peel/forcerise5_1014/policy_epoch_1000_seed_233.ckpt --policy ForceRISE5 --calib /aidata/zihao_6024/ckpts/task_0701_peel/forcerise5_1014/calib --data_path /aidata/zihao_6024/data/peel --num_obs_force 200 --num_action 20 --force_feature_dim 64 --num_inference_step 20 --voxel_size 0.005 --obs_feature_dim 512 --hidden_dim 512 --nheads 8 --num_encoder_layers 4 --num_decoder_layers 1 --dim_feedforward 2048 --dropout 0.1 --max_steps 300 --seed 233 --vis --discretize_rotation --ensemble_mode act --vis