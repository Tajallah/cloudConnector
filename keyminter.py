import rsa

#ask for a filename and then save the keypair to that file
def main():
    filename = input("Enter the filename for the keypair: ")
    (pubkey, privkey) = rsa.newkeys(512)
    with open(filename, 'w') as file:
        file.write(privkey.save_pkcs1().decode('utf-8'))
    with open(filename + ".pub", 'w') as file:
        file.write(pubkey.save_pkcs1().decode('utf-8'))
    print("Keypair saved to " + filename + " and " + filename + ".pub")

main()