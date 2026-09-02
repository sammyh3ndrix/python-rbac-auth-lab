from main import validate_password, password_hash, verify_password
from main import save_users, load_users
from main import authenticate_user
from datetime import datetime, timezone
import pytest

@pytest.fixture
def fake_users():
    fresh_fake_users = {
            "testsuser" :{
                "password" : password_hash("HYacinth@@1233"),
                "attempts" : 0,
                "locked" : False,
                "role" : "root",
                "last_login" : None

            }
        }
    return fresh_fake_users
    

def test_valid_password():
    valid_password = "Hyacinth@123"
    test_password = validate_password(valid_password)
    assert test_password == True
def test_invalid_password():
    invalid_password = "hello111"
    tests_wrong_password = validate_password(invalid_password)
    assert tests_wrong_password == False
def test_special_character():
    non_valid_special_char = [
        "hyacinth", "hyacinth@1", "he=i", "Hyacinth"
    ]
    for value in non_valid_special_char:
        test_non_special_char = validate_password(value)
        assert test_non_special_char == False
def test_verify_correct_password():
    plaintext_password = "Hyacinth@123"
    stored_hash = password_hash(plaintext_password)
    verification_result = verify_password(plaintext_password, stored_hash)
    assert verification_result == True
def test_verify_incorrect_password():
    plaintext_correct_password = "Hyacinth@123"
    stored_correct_hash = password_hash(plaintext_correct_password)
    plaintext_wrong_password = "HHYYacinth@123"
    inocrrect_verification_result = verify_password(plaintext_wrong_password, stored_correct_hash)
    assert inocrrect_verification_result == False



def test_save_and_load_persistence(tmp_path, fake_users):
    test_file = tmp_path / "test_users.json"
    save_users(fake_users, test_file)
    loaded_test_user = load_users(test_file)
    assert fake_users == loaded_test_user
def test_authenticate_user(fake_users):
    login_result = authenticate_user(fake_users, "testsuser", "helloSS@")
    assert login_result == False
    assert fake_users["testsuser"]["attempts"] == 1
def test_lockout_branch(fake_users):
    fake_users["testsuser"]["attempts"] = 2
    login_lock_result = authenticate_user(fake_users, "testsuser", "helloSS@")
    assert login_lock_result == False
    assert fake_users["testsuser"]["attempts"] == 3
    assert fake_users["testsuser"]["locked"] == True 
def test_correct_authenticate(fake_users):
        fake_users["testsuser"]["attempts"] = 2
        login_correct_result = authenticate_user(fake_users, "testsuser", "HYacinth@@1233")
        assert login_correct_result == True
        assert fake_users["testsuser"]["locked"] == False
        assert fake_users["testsuser"]["last_login"] != None
        assert fake_users["testsuser"]["attempts"] == 0
def test_locked_user(fake_users):
    fake_users["testsuser"]["locked"] =  True
    fake_users["testsuser"]["attempts"] = 3
    login_auto_reject_result = authenticate_user(fake_users, "testsuser", "HYacinth@@1233")
    assert login_auto_reject_result == False
    assert fake_users["testsuser"]["last_login"] == None
    assert fake_users["testsuser"]["attempts"] == 3
    assert fake_users["testsuser"]["locked"] == True























