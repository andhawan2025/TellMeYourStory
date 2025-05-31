import gradio_client

client = gradio_client.Client("black-forest-labs/Flux.1-schnell")

def generate_scene_image(scene_prompt):
    

    result = client.predict (
        prompt = scene_prompt,
        seed = 0,
        randomize_seed = True,
        width=1024,
        height=1024,
        num_inference_steps=4,
        api_name = "/infer"
    )

    return result


