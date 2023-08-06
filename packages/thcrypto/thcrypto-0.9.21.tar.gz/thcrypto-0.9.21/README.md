[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]



# thcrypto

## Overview

TangledHub library for cryptography.

## Licencing

thcrypto is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details.

## Installation
```bash
pip install thcrypto
```

---

## Testing
```bash
docker-compose build --no-cache thcrypto-test ; docker-compose run --rm thcrypto-test
```

## Building
```bash
docker-compose build thcrypto-build ; docker-compose run --rm thcrypto-build
```

## Publish
```bash
docker-compose build thcrypto-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thcrypto-publish
```

---

## API

thcrypto api is using the **thresult** library, so all api functions are returning result wrapped in **Ok** or **Err**
object.  
Therefore, in order to reach into the result object, you should use **.unwrap()** as in examples.

---

## Bcrypt

### cls.generate() -> Bcrypt

Generate bcrypt salt with custom parameters (4 < rounds: int > 31, prefix: bytes elem {b'2a', b'2b'}.  
If custom parameters are not passed, default values are used.

#### Example:

```python
bcrypt_default: Bcrypt = Bcrypt.generate().unwrap()

bcrypt_custom: Bcrypt = Bcrypt.generate(rounds=12, prefix=b'2b').unwrap()
```

### cls.load_or_generate() -> Bcrypt

Load bcrypt from file, if file does not exist, generate bcrypt key and writes it down to the file.  
This function can be called without parameters (in which case it is going to use default params  
**(path: str='bcrypt.salt', rounds: int=12, prefix: bytes=b'2b'))**  
or with custom params:  
**(path: str='custom_path', 4 < rounds: int > 31, prefix: bytes elem {b'2a', b'2b'})**.  
In case that bcrypt is loaded from existing file, passed custom 'rounds' and 'prefix' params are ignored.

#### Example:

```python
bcrypt_: Bcrypt = Bcrypt.load_or_generate_file().unwrap()

bcrypt_: Bcrypt = Bcrypt.load_or_generate_file(path='bcrypt.salt', 
                                               rounds=12, 
                                               prefix=b'2b').unwrap()
```

### self.get_hashed_password() -> bytes

Hash password function accepts parameter(unhashed_password: bytes | str) which has to be max 72 bytes long.

#### Example:

```python
hashed_password: bytes = bcrypt_.get_hashed_password(bcrypt_, 'test bcrypt').unwrap()
```

### cls.check_password() -> bool

Check password function accepts parameters(unhashed_password: bytes | str, hashed_password: bytes | str)

#### Example:

```python
result: bool = Bcrypt.check_password('test bcrypt', hashed_password).unwrap()
```

---

## Edd25519

### cls.generate() -> Ed25519

Generate Ed25519

#### Example:

```python
generated_ed25519: Ed25519 = Ed25519.generate().unwrap()
```

### cls.load_or_generate_file() -> Ed25519

Load ed25519 keys from files - if files not exists then generates Ed25519, writes private and public keys to the files and returns Ed25519.  
Parameters:  
**(private_path: str='custom_private_path.pem', public_path: str='custom_public_path.pem')**  
are optional, if not passed then default params are used  
**(private_path: str='sk_ed25519.pem', public_path: str='pk_ed25519.pem')**

#### Example:

```python
ed25519_: Ed25519 = Ed25519.load_or_generate_file().unwrap()

ed25519_: Ed25519 = Ed25519.load_or_generate_file(private_path='custom_path_to_sk_ed25519.pem',
                                                  public_path='custom_path_to_pk_ed25519.pem').unwrap()
```

### self.sign(data: bytes) -> bytes

Sign data with ed25519 private key

#### Example:

```python
signed_data: bytes = ed25519_.sign(data=b'test_test_b').unwrap()
```

### self.verify(signature: bytes, data: bytes) -> bool

Verify signature with ed25519 public key

#### Example:

```python
verified: bool = ed25519_.verify(signature=signed_data, data=b'test_test_b').unwrap()
```

### self.get_raw_private_key_bytes() -> bytes

Get serialized bytes from the private key.

#### Example:

```python
raw_private_key_bytes: bytes = ed25519_.get_raw_private_key_bytes().unwrap()
```

### self.get_raw_private_key() -> str

Get serialized bytes from the private key decoded to string

#### Example:

```python
raw_private_key_string: str = ed25519_.get_raw_private_key().unwrap()
```

### self.get_raw_private_key_bytes() -> bytes

Get serialized bytes from the private key.

#### Example:

```python
raw_public_key_bytes: bytes = ed25519_.get_raw_public_key_bytes().unwrap()
```

### self.get_raw_private_key() -> str

Get serialized bytes from the private key decoded to string

#### Example:

```python
raw_private_key_string: str = ed25519_.get_raw_public_key().unwrap()
```

---

## Secp2561

### cls.generate() -> Secp2561

Generate Secp2561

#### Example:

```python
generated_secp256k1: Secp2561 = Secp2561.generate().unwrap()
```

### cls.load_or_generate_file(private_path: str=None, public_path: str=None) -> Secp2561

Load secp256k1 keys from files - if files not exists then generates Secp2561, writes private and public keys to the 
files and returns Secp2561.  
Parameters:  
**(private_path: str='custom_private_path.pem', public_path: str='custom_public_path.pem')**  
are optional, if not passed then default params are used:  
**(private_path: str='sk_secp256k1.pem', public_path: str='pk_secp256k1.pem')**

#### Examples:

```python
secp256k1_: Secp2561 = Secp2561.load_or_generate_file().unwrap()

secp256k1_: Secp2561 = Secp2561.load_or_generate_file(private_path='custom_path_to_sk_secp256k1.pem',
                                                      public_path='custom_path_to_pk_secp256k1.pem').unwrap()
```

### self.sign(data: bytes) -> bytes

Sign data with SECP256K1 private key

#### Example:

```python
signed_data: bytes = secp256k1_.sign(data=b'test_test_b').unwrap()
```

### self.verify(signature: bytes, data: bytes) -> bool

Verify signature with SECP256K1 public key

#### Example:

```python
verified: bool = secp256k1_.verify(signature=b'signed_data', data=b'test_test_b').unwrap()
```

---

## Rand

### gen_random_int(bits: int) -> int

Generate a random integer, based on passed number of bits

#### Example:

```python
random_int_bits: int = gen_random_int(bits=256).unwrap()
```

### gen_random_int_hex(bits: int) -> str

Generate random string, based on passed number of bits

#### Example:

```python
random_int_hex: str = gen_random_int_hex(bits=256).unwrap()
```

### gen_random_int_hex_bytes(bits: int) -> bytes

Generate random string, based on passed number of bits

#### Example:

```python
random_int_hex_bytes: bytes = gen_random_int_hex_bytes(bits=128).unwrap()
```

### gen_random_int128(bits: int) -> int

Generate a random integer, based on 128 bits

#### Example:

```python
random_int_128: int = gen_random_int128().unwrap()
```

### gen_random_int128_hex(bits: int) -> str

Generate random string, based on 128 bits

#### Example:

```python
random_int_128_hex: str = gen_random_int128_hex().unwrap()
```

### gen_random_int128_hex_bytes(bits: int) -> bytes

Generate random bytes, based on 128 bits

#### Example:

```python
random_int_128_hex_bytes: bytes = gen_random_int128_hex_bytes().unwrap()
```

### gen_random_int256(bits: int) -> int

Generate a random integer, based on 256 bits

#### Example:

```python
random_int_256: int = gen_random_int256().unwrap()
```

### gen_random_int256_hex(bits: int) -> str

Generate random string, based on 256 bits

#### Example:

```python
random_int_256_hex: str = gen_random_int256_hex().unwrap()
```

### gen_random_int256_hex_bytes(bits: int) -> bytes

Generate random bytes, based on 256 bits

#### Example:

```python
random_int_256_hex_bytes: bytes = gen_random_int256_hex_bytes().unwrap()
```

---

## Fernet

### cls.generate(cls) -> Fernet

Generate Fernet

#### Example:

```python
generated_fernet: Fernet = Fernet.generate().unwrap()
```

### cls.load_or_generate_file(path: str='fernet.key') -> Fernet

Load Fernet from file or generate one This function tries to load the Fernet from file, if file does not exist then generate Fernet and writes it down to a file.  
Function accepts optional 'path' parameter **(path: str='custom_path.key')** or uses default value **(path: str='fernet.key')**

#### Example:

```python
fernet_: Fernet = Fernet.load_or_generate_file().unwrap()

fernet_: Fernet = Fernet.load_or_generate_file(path='custom_path_fernet.key').unwrap()
```

### self.encrypt_bytes(data_bytes: bytes, current_time: int | None=None) -> bytes

Encrypt bytes with Fernet key This function takes required argument 'data_bytes' and optional argument 'current_time'

#### Example:

```python
encrypted_bytes: bytes = fernet_.encrypt_bytes(data_bytes=b'test bytes', 
                                               current_time=int(time())).unwrap()
```

### self.decrypt_bytes(enc_data_bytes: bytes, ttl: int | None=None, current_time: int | None=None) -> bytes

Decrypt bytes with Fernet key.  
This function takes required argument 'enc_data_bytes' and two optional arguments 'ttl' and 'current_time'

#### Example:

```python
decrypt_bytes: bytes = fernet_.decrypt_bytes(enc_data_bytes=encrypted_bytes, 
                                             ttl=100, 
                                             current_time=int(time())).unwrap()
```

### self.encrypt_dict(data_dict: dict, current_time: int | None=None) -> str

Encrypt bytes with Fernet key This function takes required argument 'data_bytes' and optional argument 'current_time'

#### Example:

```python
encrypted_dict: str = fernet_.encrypt_dict(data_dict={'test_key': 'test_value'}, current_time=int(time())).unwrap()
```

### self.decrypt_dict(enc_data_str: str, ttl: int | None=None, current_time: int | None=None) -> dict

Decrypt bytes with Fernet key.  
This function takes required argument 'data_bytes' and two optional arguments 'ttl' and 'current_time'

#### Example:

```python
decrypted_dict: dict = fernet_.decrypt_dict(enc_data_str=encrypted_dict, ttl=100, current_time=int(time())).unwrap()
```

---

## Multifernet

Create Multifernet instance

#### Example:

```python
fernet_key_1: Fernet = Fernet.generate().unwrap()
multi_fernet_1: MultiFernet = MultiFernet([fernet_key_0])
```

### self.encrypt_bytes(data_bytes: bytes, current_time: int | None=None) -> bytes

Encrypt bytes. This function takes required argument 'data_bytes' and optional argument 'current_time'

#### Example:

```python
encrypted_bytes: bytes = multi_fernet_1.encrypt_bytes(data_bytes=b'12345', current_time=int(time())).unwrap()
```

### self.decrypt_bytes(enc_data_bytes: bytes, ttl: int | None=None, current_time: int | None=None) -> bytes

Decrypt bytes. This function takes required argument 'enc_data_bytes' and two optional arguments 'ttl' and '
current_time'

#### Example:

```python
decrypted_bytes: bytes = multi_fernet_1.decrypt_bytes(enc_data_bytes=encrypted_bytes, ttl=100,
                                                      current_time=int(time())).unwrap()
```

### self.encrypt_dict(data_dict: dict, current_time: int | None=None) -> str

Encrypt dict. This function takes required argument 'data_dict' and optional argument 'current_time'

#### Example:

```python
encrypted_dict: str = multi_fernet_1.encrypt_dict(data_dict={'test_key': 'test_value'},
                                                  current_time=int(time())).unwrap()
```

### self.decrypt_dict(enc_data_str: str, ttl: int | None=None, current_time: int | None=None) -> dict

Decrypt dict. This function takes required argument 'enc_data_bytes' and two optional arguments 'ttl' and 'current_time'

#### Example:

```python
decrypted_dict: dict = multi_fernet_1.decrypt_dict(enc_data_str=encrypted_dict, ttl=100,
                                                   current_time=int(time())).unwrap()
```

### self.add_fernet(fernet: Fernet) -> MultiFernet

Add new fernet. This function takes required argument 'fernet' and returns new instance of MultiFernet with new fernet
key added to beginning of fernet key list

#### Example:

```python
fernet_key_2: Fernet = Fernet.generate().unwrap()
multi_fernet_2: MultiFernet = multi_fernet_1.add_fernet(fernet_key_2).unwrap()
```

### self.rotate(enc_data_bytes: bytes) -> bytes

Rotate fernet keys (re-encrypt token)

#### Example:

```python
rotated_msg_with_multi_fernet_2: bytes = multi_fernet_2.rotate(encrypted_bytes).unwrap()
```

<!-- Links -->

<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green

[pypi-project-url]: https://pypi.org/project/thcrypto/
[stable-ver-image]: https://img.shields.io/pypi/v/thcrypto?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thcrypto.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thcrypto.svg

