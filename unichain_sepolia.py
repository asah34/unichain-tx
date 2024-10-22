from web3 import Web3
import time
import os
import random
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style, init

import secrets
from eth_utils import to_checksum_address

def generate_eth_address():
    # Generate a random 20-byte (160-bit) address
    random_bytes = secrets.token_bytes(20)
    # Convert to Ethereum checksum address
    return to_checksum_address('0x' + random_bytes.hex())

# Generate a list of random Ethereum addresses
receivers = [generate_eth_address() for _ in range(5)]  # Ganti 5 dengan jumlah yang diinginkan

# Inisialisasi colorama
init(autoreset=True)

# Karakter khusus
CHECK_MARK = Fore.GREEN + "✔️" + Style.RESET_ALL
CROSS_MARK = Fore.RED + "❌" + Style.RESET_ALL
SPECIAL_CHAR = Fore.YELLOW + "★" + Style.RESET_ALL
BALANCE_SYMBOL = Fore.CYAN + "💰" + Style.RESET_ALL
GWEI_SYMBOL = Fore.MAGENTA + "⛽ Gwei:" + Style.RESET_ALL
GAS_PRICE_SYMBOL = Fore.BLUE + "⛽ Gas Price:" + Style.RESET_ALL
ETH_SYMBOL = Fore.YELLOW + "Ξ" + Style.RESET_ALL
SENDER_ADDRESS_SYMBOL = Fore.CYAN + "📤 Alamat Pengirim:" + Style.RESET_ALL
RECEIVER_ADDRESS_SYMBOL = Fore.MAGENTA + "📥 Alamat Penerima:" + Style.RESET_ALL
AMOUNT_SYMBOL = Fore.LIGHTYELLOW_EX + "💵 Jumlah Kiriman:" + Style.RESET_ALL

# Muat variabel dari file .env
load_dotenv()

# Koneksi ke node Ethereum
web3 = Web3(Web3.HTTPProvider('https://autumn-cosmological-scion.unichain-sepolia.quiknode.pro/c568806873f2a9edb9fcdea8aef0569ff729eb25'))

if web3.is_connected():
    print(Fore.GREEN + f"Terkoneksi dengan jaringan Ethereum {CHECK_MARK}")
else:
    print(Fore.RED + f"Gagal terhubung ke jaringan Ethereum {CROSS_MARK}")
    raise Exception("Gagal terhubung ke jaringan Ethereum")

# Alamat dan kunci pribadi dari pengirim
sender_address = os.getenv('SENDER_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

if not sender_address or not private_key:
    raise Exception(f"{CROSS_MARK} Harap isi SENDER_ADDRESS dan PRIVATE_KEY di file .env")

# Daftar penerima random ETH
receivers = [
    generate_eth_address() for _ in range(1000) 
    # Ganti 1000 dengan jumlah yang diinginkan
]

def get_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')


def get_nonce():
    return web3.eth.get_transaction_count(sender_address)


def get_gas_price():
    return web3.eth.gas_price


def send_transaction(receiver_address, amount, gas_price):
    # Dapatkan nonce terbaru
    nonce = get_nonce()

    
    sender_balance_before = get_balance(sender_address)
    print(Fore.BLUE + f"{BALANCE_SYMBOL} Saldo Pengirim Sebelum Tx: {sender_balance_before} {ETH_SYMBOL}")
    print(Fore.CYAN + f"{SENDER_ADDRESS_SYMBOL} {sender_address}")
    print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address}")
    print(Fore.LIGHTYELLOW_EX + f"{AMOUNT_SYMBOL} {web3.from_wei(amount, 'ether')} {ETH_SYMBOL}")

   
    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': amount,
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 1301
    }

    
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    try:
       
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)
        print(Fore.CYAN + f"{datetime.now()} - Transaksi berhasil ke {receiver_address}. {CHECK_MARK}")

       
        sender_balance_after = get_balance(sender_address)
        print(Fore.YELLOW + f"{BALANCE_SYMBOL} Saldo Pengirim Setelah Tx: {sender_balance_after} {ETH_SYMBOL}")
        print(Fore.BLUE + f"{SENDER_ADDRESS_SYMBOL} {sender_address} {CHECK_MARK}")
        print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address} {CHECK_MARK}\n")

    except Exception as e:
        print(Fore.RED + f"Gagal mengirim transaksi: {str(e)} {CROSS_MARK}")


while True:
    for receiver in receivers:
        # Acak jumlah transfer dari min hingga max (misal 0.000000001 ETH hingga 0.00000002 ETH)
        random_amount = web3.to_wei(random.uniform(0.000000001, 0.00000002), 'ether')

       
        gas_price = get_gas_price()
        print(Fore.MAGENTA + f"{GAS_PRICE_SYMBOL} {web3.from_wei(gas_price, 'gwei')} {GWEI_SYMBOL}")

       
        send_transaction(receiver, random_amount, gas_price)

        
        time.sleep(10)
    
   
    print(Fore.YELLOW + f"Menunggu 1 menit sebelum pengiriman berikutnya {SPECIAL_CHAR}...")
    time.sleep(60)
