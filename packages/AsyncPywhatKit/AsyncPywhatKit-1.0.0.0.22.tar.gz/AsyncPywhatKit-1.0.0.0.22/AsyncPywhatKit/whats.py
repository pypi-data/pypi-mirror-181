import time
import webbrowser as web
from datetime import datetime
from re import fullmatch
from typing import List
from urllib.parse import quote
import asyncio
import pyautogui as pg
import asyncio
from AsyncPywhatKit.Core import core,log,exceptions

pg.FAILSAFE = False

async def main():
    await core.check_connection()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


async def sendwhatmsg_instantly(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message Instantly"""

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}\s?[0-9]{10}$", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    await asyncio.sleep(4)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    await asyncio.sleep(wait_time - 4)
    await core.findtextbox()
    pg.press("enter")
    await log.log_message(_time=time.localtime(), receiver=phone_no, message=message)
    if tab_close:
        await core.close_tab(wait_time=close_time)


async def sendwhatmsg(
    phone_no: str,
    message: str,
    time_hour: int,
    time_min: int,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send a WhatsApp Message at a Certain Time"""
    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    phone_no = phone_no.replace(" ", "")
    if not fullmatch(r"^\+?[0-9]{2,4}[0-9]{10}$", phone_no):
        raise exceptions.InvalidPhoneNumber("Invalid Phone Number.")

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    await asyncio.sleep(sleep_time)
    await core.send_message(message=message, receiver=phone_no, wait_time=wait_time)
    await log.log_message(_time=current_time, receiver=phone_no, message=message)
    if tab_close:
        await core.close_tab(wait_time=close_time)


async def sendwhatmsg_to_group(
    group_id: str,
    message: str,
    time_hour: int,
    time_min: int,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message to a Group at a Certain Time"""

    if time_hour not in range(25) or time_min not in range(60):
        raise Warning("Invalid Time Format!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Message will be Delivered!"
    )
    await asyncio.sleep(sleep_time)
    await core.send_message(message=message, receiver=group_id, wait_time=wait_time)
    await log.log_message(_time=current_time, receiver=group_id, message=message)
    if tab_close:
        await core.close_tab(wait_time=close_time)


async def sendwhatmsg_to_group_instantly(
    group_id: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send WhatsApp Message to a Group Instantly"""

    current_time = time.localtime()
    await asyncio.sleep(4)
    await core.send_message(message=message, receiver=group_id, wait_time=wait_time)
    await log.log_message(_time=current_time, receiver=group_id, message=message)

    if tab_close:
        await core.close_tab(wait_time=close_time)


async def sendwhatsmsg_to_all(
    phone_nos: List[str],
    message: str,
    time_hour: int,
    time_min: int,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
):
    for phone_no in phone_nos:
        await sendwhatmsg(
            phone_no, message, time_hour, time_min, wait_time, tab_close, close_time
        )


async def sendwhats_image(
    receiver: str,
    img_path: str,
    time_hour: int,
    time_min: int,
    caption: str = "",
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send Image to a WhatsApp Contact or Group at a Certain Time"""

    if (not receiver.isalnum()) and (not core.check_number(number=receiver)):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    current_time = time.localtime()
    left_time = datetime.strptime(
        f"{time_hour}:{time_min}:0", "%H:%M:%S"
    ) - datetime.strptime(
        f"{current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}",
        "%H:%M:%S",
    )

    if left_time.seconds < wait_time:
        raise exceptions.CallTimeException(
            "Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!"
        )

    sleep_time = left_time.seconds - wait_time
    print(
        f"In {sleep_time} Seconds WhatsApp will open and after {wait_time} Seconds Image will be Delivered!"
    )
    await asyncio.sleep(sleep_time)
    await core.send_image(

        path=img_path, caption=caption, receiver=receiver, wait_time=wait_time
    )
    await log.log_image(_time=current_time, path=img_path, receiver=receiver, caption=caption)
    if tab_close:
        await core.close_tab(wait_time=close_time)


async def open_web() -> bool:
    """Opens WhatsApp Web"""

    try:
        web.open("https://web.whatsapp.com")
    except web.Error:
        return False
    else:
        return True
