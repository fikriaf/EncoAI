from transformers import AutoModelForCausalLM, AutoTokenizer

def get_response(input_text):
    model_name = "gpt2"  # GPT-2 model (contoh saja, Anda bisa menggunakan model lain)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Preprocessing teks masukan
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Menghasilkan respons dari model
    with torch.no_grad():
        output = model.generate(input_ids, max_length=50, pad_token_id=tokenizer.eos_token_id)

    # Decode hasil output menjadi teks
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response

# Pengujian
while True:
    user_input = input("Anda: ")
    if user_input.lower() == "exit":
        print("Chat berakhir.")
        break
    response = get_response(user_input)
    print("AI:", response)
