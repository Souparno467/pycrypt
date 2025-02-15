from flask import Flask, render_template, request
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data['message']
    encryption_type = data['encryption_type']

    if encryption_type == 'AES':
        key = get_random_bytes(16).hex()  # Generate AES key
        nonce = get_random_bytes(16).hex()  # Generate nonce
        cipher = AES.new(bytes.fromhex(key), AES.MODE_EAX, nonce=bytes.fromhex(nonce))
        ciphertext, tag = cipher.encrypt_and_digest(message.encode())

        return render_template(
            'encrypt_result.html',
            ciphertext=ciphertext.hex(),
            key=key,
            nonce=nonce
        )

    return "Unsupported encryption type", 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    ciphertext = data['ciphertext']
    key = data['key']
    nonce = data['nonce']
    decryption_type = data['decryption_type']

    if decryption_type == 'AES':
        cipher = AES.new(bytes.fromhex(key), AES.MODE_EAX, nonce=bytes.fromhex(nonce))
        plaintext = cipher.decrypt(bytes.fromhex(ciphertext)).decode()
        return render_template('decrypt_result.html', plaintext=plaintext)

    return "Unsupported decryption type", 400

if __name__ == '__main__':
    app.run(debug=True)
