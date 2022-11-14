# Nowcasting-of-extreme-precipitation


![4_overall model_big](https://user-images.githubusercontent.com/37731007/201572457-492baf0f-d7dc-43a4-b5a3-bc5e75168fac.png)

"Bechmark test" contains scripts used for running PySTEPS, more detail can be found at: https://github.com/RubenImhoff/Large_Sample_Nowcasting_Evaluation

"event selection and data analysis" contains scripts used for selecting extreme precipitation events and analyze the precipitation data

"vqgan+transformer" contains the main scripts for the model, which is based on another opensource project avavilable at https://github.com/lucidrains/nuwa-pytorch. The folder includs scripts of the modified model structure and the conducted experiments

The code can be used following the steps below: 
1. Download the precipitation data, install nuwa-pytorch and PySTEPS
2. Use event selection and data analysis/event_selection_extreme_opti to calculate the catchment-averaged precipitation accumulation of all possible events
3. Use event selection and data analysis/event_selection_function to find the threshold of extreme precipitation events and generate the training/validation/testing set
4. Use vqgan+transformer/vqgan_training to train the VQGAN, which is the first stage of the model
5. With the trained VQGAN, transform the radar data to latent space token sequences
6. Use vqgan+transformer/transformer_training to train the autoregressive transformer, which is the second stage of the model
7. Use vqgan+transformer/experiment_nowcasting to test the model's ability of producing nowcasting result
8. Use vqgan+transformer/experiment_extreme_detection to test the model's ability of detecting the defined extreme events
