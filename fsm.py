from os import truncate
from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message
from linebot.models import MessageTemplateAction

# global variable
to_jail = False
to_backdoor = False
to_kitchen = False
to_hall = False
explore_kitchen = False
leave_kitchen = False
to_sword_room = False
to_armor_room = False
to_bedroom = False
have_key = False
explore_bedroom = False
leave_bedroom = False
to_outside = False
to_secret_room = False
wrong_answer = False
correct_answer = False
have_sword = False
have_armor = False
to_lawn = False
to_gate = False
to_warehouse = False

is_dead = False
is_win = False
is_restart = False

score = 0


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def on_enter_user(self):
        # initialize global variables
        global to_jail, to_backdoor, to_kitchen, to_hall, explore_kitchen, leave_kitchen, to_sword_room
        global to_armor_room, to_bedroom, have_key, explore_bedroom, leave_bedroom, to_outside
        global to_secret_room, wrong_answer, correct_answer, have_sword, have_armor, to_lawn
        global to_gate, to_warehouse, is_dead, is_win, is_restart, score
        to_jail = False
        to_backdoor = False
        to_kitchen = False
        to_hall = False
        explore_kitchen = False
        leave_kitchen = False
        to_sword_room = False
        to_armor_room = False
        to_bedroom = False
        have_key = False
        explore_bedroom = False
        leave_bedroom = False
        to_outside = False
        to_secret_room = False
        wrong_answer = False
        correct_answer = False
        have_sword = False
        have_armor = False
        to_lawn = False
        to_gate = False
        to_warehouse = False

        is_dead = False
        is_win = False
        is_restart = False

        score = 0

    def is_going_to_jail(self, event):
        global to_jail
        text = event.message.text
        if text.lower() == "start game" or text == 'leave' or text == 'The door is locked! Return to jail':
            to_jail = True
        return to_jail

    def on_enter_jail(self, event):
        text = 'which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='backdoor(right)',
                text='backdoor'
            ),
            MessageTemplateAction(
                label='kitchen(forward)',
                text='kitchen'
            ),
            MessageTemplateAction(
                label='hall(left)',
                text='hall'
            ),
        ]
        url = 'https://static.vecteezy.com/system/resources/thumbnails/001/312/495/small/jail-and-prison-cell-background-free-vector.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_backdoor(self, event):
        global to_backdoor
        text = event.message.text
        if text == 'backdoor':
            to_backdoor = True
        return to_backdoor

    def is_going_to_kitchen(self, event):
        global to_kitchen
        text = event.message.text
        if text == 'kitchen':
            to_kitchen = True
        return to_kitchen

    def is_going_to_hall(self, event):
        global to_hall
        text = event.message.text
        if (text == 'hall' or text == 'leave'):
            to_hall = True
        return to_hall

    def on_enter_backdoor(self, event):
        text = 'The door is locked! Return to jail'

        send_text_message(event.reply_token, text)

    def on_enter_kitchen(self, event):
        text = 'You\'ve enter the kitchen. What do you want to do?'
        btn = [
            MessageTemplateAction(
                label='explore',
                text='explore'
            ),
            MessageTemplateAction(
                label='leave',
                text='leave'
            ),
        ]
        url = 'https://graphicriver.img.customer.envatousercontent.com/files/268608494/preview_11687188.jpg?auto=compress%2Cformat&q=80&fit=crop&crop=top&max-h=8000&max-w=590&s=3cc7cd99bcedd0a04565830526921ed1'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_kitchen(self, event):
        global explore_kitchen
        text = event.message.text
        if text == 'explore':
            explore_kitchen = True
        return explore_kitchen

    def on_enter_explore_kitchen(self, event):
        global score
        text = 'You\'ve found a lobster! 50 points get!'
        score += 50
        url = 'https://st2.depositphotos.com/1713003/47492/v/950/depositphotos_474928178-stock-illustration-red-lobster-vector-illustration.jpg'
        send_text_message(event.reply_token, text)

    # def is_leaving_kitchen(self, event):
    #     global leave_kitchen
    #     text = event.message.text
    #     if text == 'leave':
    #         leave_kitchen = True
    #     return leave_kitchen

    def on_enter_hall(self, event):
        text = 'You\'ve entered the hall. Which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='sword room',
                text='sword room(left)'
            ),
            MessageTemplateAction(
                label='armor room',
                text='armor room(forward)'
            ),
            MessageTemplateAction(
                label='bedroom',
                text='bedroom(right)'
            ),
        ]
        url = 'https://media.istockphoto.com/vectors/vector-old-hall-room-with-stairs-doors-and-a-window-cartoon-vector-id1256874566?k=20&m=1256874566&s=170667a&w=0&h=NMclArE3rh9teJRgWPS-ng8LlShu1rlzNJknnRvGLI8='
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_sword_room(self, event):
        global to_sword_room
        text = event.message.text
        if text == 'sword room(left)':
            to_sword_room = True
        return to_sword_room

    def is_going_to_armor_room(self, event):
        global to_armor_room
        text = event.message.text
        if text == 'armor room(forward)':
            to_armor_room = True
        return to_armor_room

    def is_going_to_bedroom(self, event):
        global to_bedroom
        text = event.message.text
        if text == 'bedroom(right)':
            to_bedroom = True
        return to_bedroom

    def on_enter_sword_room(self, event):
        global have_key
        if not have_key:
            text = 'The room is locked.'
            send_text_message(event.reply_token, text)
        else:
            global score
            text = 'You\'ve entered the sword room and finded a sword there. 100 points get!\nHowever, the monster is waken up by the noise and it\'s now at the outside of the sword room.\nYou need to find another way out, and QUICK!'
            score += 100
            btn = [
                MessageTemplateAction(
                    label='outside',
                    text='There\'s a window, jump outside!'
                ),
                MessageTemplateAction(
                    label='secret room',
                    text='At the corner of the wall, some stones are cracking. Ah-ha! There\'s a secret passage'
                ),
            ]
            url = 'https://previews.123rf.com/images/klyaksun/klyaksun1907/klyaksun190700278/128801904-museum-exhibition-room-cartoon-vector-illustration-palace-interior-art-gallery-of-medieval-castle-em.jpg'
            send_button_message(event.reply_token, text, btn, url)

    def on_enter_armor_room(self, event):
        global score
        text = 'You\'ve entered the armor room and finded an armor there. 50 points get!\nHowever, the monster is waken up by the noise and it\'s now at the outside of the armor room.\nYou need to find another way out, and QUICK!'
        score += 50
        btn = [
            MessageTemplateAction(
                label='outside',
                text='There\'s a window, jump outside!'
            ),
            MessageTemplateAction(
                label='secret room',
                text='At the corner of the wall, some stones are cracking. Ah-ha! There\'s a secret passage'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/medieval-castle-throne-room-ballroom-interior-with-knights-armor-both-sides-king_33099-892.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def on_enter_bedroom(self, event):
        text = 'You\'ve entered the monster\'s bedroom.\nIt is asleep now. BE QUIET!\nWhat do you want to do?'
        btn = [
            MessageTemplateAction(
                label='leave',
                text='leave'
            ),
            MessageTemplateAction(
                label='explore',
                text='explore'
            ),
        ]
        url = 'https://media.istockphoto.com/photos/3d-rendering-of-classic-bedroom-apartment-in-the-moonlight-picture-id1269267277?k=20&m=1269267277&s=612x612&w=0&h=12iCGNCLc5tDPc9BxE0HlTo1b3TN_rqgEVt2NLJ6f3Q='
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_explore_bedroom(self, event):
        global explore_bedroom
        text = event.message.text
        if text == 'explore':
            explore_bedroom = True
        return explore_bedroom

    def on_enter_explore_bedroom(self, event):
        global have_key
        text = 'You\'ve found a key! Who knows what is the key for?'
        have_key = True
        url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk3zCxojxTkYRzk46Row09wFEv9qK0UkbYKw&usqp=CAU'
        send_text_message(event.reply_token, text)

    # def is_leaving_bedroom(self, event):
    #     global leave_bedroom
    #     text = event.message.text
    #     if text == 'leave':
    #         leave_bedroom = True
    #     return leave_bedroom

    def is_going_to_secret_room(self, event):
        global to_secret_room
        text = event.message.text
        if text == 'At the corner of the wall, some stones are cracking. Ah-ha! There\'s a secret passage':
            to_secret_room = True
        return to_secret_room

    def on_enter_secret_room(self, event):
        text = 'You\'ve found a secret room. there\'s three boxes at front.\nFind the different one among the three. (Hint: Jay Chou)'
        btn = [
            MessageTemplateAction(
                label='黑色毛衣',
                text='黑色毛衣'
            ),
            MessageTemplateAction(
                label='黑色柳丁',
                text='黑色柳丁'
            ),
            MessageTemplateAction(
                label='黑色幽默',
                text='黑色幽默'
            ),
        ]
        url = 'https://png.pngtree.com/png-clipart/20200225/original/pngtree-3d-black-box-with--tape-vector-illustration-png-image_5268211.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_wrong_answer(self, event):
        global wrong_answer
        text = event.message.text
        if text == '黑色毛衣' or text == '黑色幽默':
            wrong_answer = True
        return wrong_answer

    def is_going_to_correct_answer(self, event):
        global correct_answer
        text = event.message.text
        if text == '黑色柳丁':
            correct_answer = True
        return correct_answer

    def on_enter_wrong_answer(self, event):
        text = 'Oh No! You made the wrong answer and triggered the trap'
        # url = 'https://st2.depositphotos.com/4464609/6699/v/950/depositphotos_66998681-stock-illustration-guillotine.jpg'
        send_text_message(event.reply_token, text)

    def on_enter_correct_answer(self, event):
        global score
        score += 250
        text = 'Nice Job! You make the right answer and open the box.\nThere\'s a diamond in the box. 250 points get!'
        # url = 'https://st2.depositphotos.com/1192512/7466/v/380/depositphotos_74660431-stock-illustration-golden-chain-necklace-with-heart.jpg?forcejpeg=true'
        send_text_message(event.reply_token, text)

    def is_going_to_outside(self, event):
        global to_outside
        global correct_answer
        text = event.message.text
        if text == 'There\'s a window, jump outside!' or correct_answer:
            to_outside = True
        return to_outside

    def on_enter_outside(self, event):
        text = 'You\'ve reached outside. Which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='lawn',
                text='lawn(left)'
            ),
            MessageTemplateAction(
                label='gate',
                text='gate(forward)'
            ),
            MessageTemplateAction(
                label='warehouse',
                text='warehouse(right)'
            ),
        ]
        url = 'data:image/jpeg;base64,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'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_lawn(self, event):
        global to_lawn
        text = event.message.text
        if text == "lawn(left)":
            to_lawn = True
        return to_lawn

    def is_going_to_gate(self, event):
        global to_gate
        text = event.message.text
        if text == "gate(forward)":
            to_gate = True
        return to_gate

    def is_going_to_warehouse(self, event):
        global to_warehouse
        text = event.message.text
        if text == "warehouse(right)":
            to_warehouse = True
        return to_warehouse

    def on_enter_lawn(self, event):
        global have_armor
        global is_dead
        global is_win
        if not have_armor:
            text = 'OUCH! There are traps in the lawn.'
            is_dead = True
            send_text_message(event.reply_token, text)
        else:
            text = 'You crouched in the lawn with your armor protecting you from the traps in the lawn, and finally escaped the house.'
            is_win = True
            # url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjRCKcJSWeqkJCqeO2vpIClwOGUtjQTg_mw&usqp=CAU'
            send_text_message(event.reply_token, text)

    def on_enter_gate(self, event):
        global have_sword
        global is_dead
        global is_win
        if not have_sword:
            text = 'There\'s a guard in front of the gate. You have no weapon to fight him.'
            is_dead = True
            send_text_message(event.reply_token, text)
        else:
            text = 'You use your sword to defeat the guard blocking the gate, and finally escaped the house.'
            is_win = True
            # url = 'https://en.pimg.jp/079/061/259/1/79061259.jpg'
            send_text_message(event.reply_token, text)

    def on_enter_warehouse(self, event):
        global is_win

        text = 'You entered the warehouse and find a car there. You use the key stolen from the bedroom, and finally escaped the house.'
        is_win = True
        url = 'data:image/png;base64,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'
        send_text_message(event.reply_token, text)

    def is_going_to_dead(self):
        return is_dead

    def is_going_to_win(self):
        return is_win

    def on_enter_win(self, event):
        global score
        text = f'Congrats! You WON!\nYour score is {score} points.\nDo you want to start again?'
        btn = [
            MessageTemplateAction(
                label='yes',
                text='yes'
            ),
            MessageTemplateAction(
                label='no',
                text='no'
            ),
        ]
        url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAABO1BMVEX////80Rb/thzznBLvSDbAOSvpwxr/sgCmOi7oxRrzmhLLRjf/uB3/sQD+tBv8rxn3pBXznhL4zhfwyBi+Lx7/uxruPin5qRfqwRnypBOiMy/usxbNPS7/5r38sBr/tRHsuhjxqBTvQS3/9+nJQDjuOSL/+/P/1Y+/MyT/2JfxpxT/5Lf/xFj/4K7/3aX/6cX/0IDttxfvrhX/897YjYjuNBq8HQD6z8v/uzH/wEb/zXb/7tP/yWn/wUrgci7aZTHwlCb0i4LoubXYgSWrPy2zOSzlRzbgnpn2pJ3wW0z3r6nzgXf2npfRb2f4vLf71NH2qFjkfCXkw7/UWDO2SxSaFxzNcyfmfiyoKRm9WirFZyi0Tivms6/diCTpmCH1npjMMR7xZVf35OPydGnGSj7NYVfUe3TRdGzuKADMIbmUAAAOSklEQVR4nO2dC1cbNxaAqU08MB4/BuLYxsZjwBiMeVO2BMirAfpI02yabbohTbebbbv7/3/BSvPUjK40M7Y0I3O4Pac9tY/t+bhXug9JV3NzsmXLONs6Ad8Zjs6MLem/L112tULBqjzeo98Zaegt7fEw+2cSKpeIAomlaecXoTf2LfcdYyOnRxMjhw6GjVI52/f1tWf4b1jaBe8bFJdRpUCKVrk8wC+vnmnky5XVvJ9zYtkLA9oKM0YHj7XIq5X9vJ90QjmgAG1Fahb1WuUw72edSC6iquKIdpn3004gGykAsdfI+3njZDg6R3J4uLU12t/fG49XVwu0MfIk8BrDk9X9w8st1fykoVm2aL6k4sOI1sHFeHT+xNAqaKha2lneSGHZTw0ECP67WL7mNbUCOkMAIAWskp0eiFBhVKzzvLEI2U03qySUCpyS5CEboGufWqzdvMF82ZJhpEgqB3mTeSLFRpFYqoQBq5JUiJQ4zpvNkSfJdWggSYNo5M1my0n8PIPBjGq11+vV0D+9XtV5JZ5QUyKvOuSr0CgY1VqzbhaLRV0v2v/G/zHrzVo1njJ/t7+xT+WzYeVVa3UTEdlsIcEvmnVMySXMN3Mc7j2B8lkCr2lCcCFMs9njQWr5FaqGe7sVDh6yzqap8+h8St1sVpmM1uPRQR6WOhzH4fXqSeh8ynqvwIDECdnZ4TjbCG58yTNObJ61ZOoLKbLGMVZLqxi7o6zKjqt8PATYM5l4OpscM/K+FlFqmYRxwzj3VwXsU3fENOttNLW6AthqNea7M3Ee/BjNMJrRR8cw7eNOv1Va9KTV73eO2zSlrjdjnEcWxeMxl7BHK6/d6SO2UlTQS/1Om1Yl11QziXH2OIRIgRG+naMSDUdglo7WIpBIjewfyCTvZxMaVTOMZ3ZaHt7y8tLSF4QsLS/7kJ16mNHkeMcnGRCOWIRGjQxfkHX2XbzlEFsI04Xst/XQR9mWqmVAyEroQxYa8C0z6MKQmDGRpVYyCOIYqYRB+gjddPiY2qMhF49IJ6rXGYhZLDaeg4RGnVTg8WIC9RHiMB6TpmrCiBqwXC5aLiFCwyT//vb8kpzPY1xsEaaqw4hZVMIhQoOwMFeBSewzZKuuGmMQs6gwAtVfwkR13R6Bafk8xsV+MB/DYzGDBRu67kQC1lupDTQQbKotYsaCEOVHpie0BgM3obfTzTAQYikYjJDTkF7qp6NSoxY80dqkFuqJbalrwRfSrl927H1IpU5GLwI4BR+WMGKxF0WUHHvvAvFMUSgghRj9OamR6YkBOAp/YhAE6CDu+N9apxA1aaX+MVC8CAah3hYE6CAGfzh6KFZ25QSnW1D1ohr455IoQBux5QdJOl3ZsCojCYDQECTCbb0lDtBG7Ad2CnnFM9ERODgESRvtLE7nJsKCnMZih2OnWI1iy/2rFTih8C1pRyigg+jPNkU4BrcElhZX4QKi0fQJp4pkIMHRjU/IyIcF7tp8DCe9wTRzJHIQOoJzYt9O4TKqwEVwRlbvqdB2FCJtFAu2Uz9CZSjREkYIp/V+NIPnUbE2igXZacu3UxhQ3JZNsMwdqBAHM8IBbTs95ipRE+cVhyAhqULRNopliVQiSChwMoXyes8X2lULCYAhJYI+UeTyMLBW4ZdmZKkwpESwaCNyKwqwoua5ClmjEAuZRwHRqdCiFFWcCeaZviwV2krss+cagRPNHLQH2I399bo8FdpK9GJ7kx6GQheEqY33VW+AdGT4Qk+QT/QCcDquEbyEEQncAiOVNs9gIR0GZabiIhpbombqGo8dsEkDtM3UDd2ocobAiMaWaFhTzMJIQ2YajdzETjTUZvyedGfoCOkSezInmuiyaJAZyjVS20wZA1HshrfoVnWvPoPdvUwjxWbq5frReo3YzbVRh+8tF8oehqGBGAnchJb3x9GgzfDGhsSAxhEirNEjc4FIf0gFNFViopEKiAdii+HzLXFLiedRQqPmDn5T9kRjTzVecTiaQQk7lknvVPemUuzv5Q5De6rxyjVUjijq/PAZvejbzGoqtQndDApYL60IqXwDRwt9Z3GcCeEx7C7ssShgzRuq0QSEsqdSezLlEQrIgsHtMx5hJxPCDiP2xjL9/poLsKDv1mhwrTtnwumH4iG4T88LabIhPGKm+SKUCO9EvEuE8LEtdcahgP01+xCiOoQizkVd8vyhfMJlrrcQU6wBYhplPL6YQ6Yn9EYvVaI2UduH6PTQzS1wOTgDwjor8i5oorbxRZ2i4Z0bMcWvbkcF/QIrexK5YTi6kK9EBiy0JhwNv5WoYojtoBVp7aFCJUr0lu+IDj13sZNfNVHwysxGjhVh76eiFWGxVf3oskU1o4FIDsPIRCN40z6VYhSzGYhBzBZdmRG935vajJH76propSdmxTS7FdKIvxfc2YVuIpTZKre/oyb6BGLXnoBtX55HlFr2JgreVIIv9lgCXcvIZLfJMm+3idhjCcCur4x2DPkbhekdQxWRJ6Cobyc2sWez6wvIfkUetoS6lWWzc8/b9AXt3BMZl8L7S71oSpYSyS204GlLgQf1wKJpFjto15jzjE0o7ngQ3DQwpEQpu6D9iRQ+jyBwz9Dd38nOasjmK1HOaQR/NxS8kV2kR7xgHJmp+YjC7TS0U5/RRELMCrAjJ2fgAo1/Cl+4nS6RB/TAFRnhvdxHUOek4ISs7RTFnuzy80KdOimLRfyVAxu7kNsPTuf1Mz2dV6jIaFQzhvo7F30ReACxRA5CcJqR1Kd+eE7NOMQJRHGHSPEX+W0owHhNXoeTC2odKuinIOwgMAYMGitAIbfUWz+o8CboamIfsxRyWp1oqwAEpBW5Pfjp/UP+KUQXccoZtUTGMmBaKLndF51mkF0j2pP0bSFlKdIYgxqEliW7yRCQKpKdP+rTd/5oBb1u9Cb9Y9L7RA0hx08gFiduT/OFY6Fkgxpg0TeDBjxnNGGhQDaJOkrfQilQIBFto2mU/qGcWgxFENdKE3dRKq2RgNDWiwzuMmG0ayMRnVZmiTqZ+Xy2AvtmDGAmhIymgmS7Nh3vs0nD6PC1SAUyGrZl0TeRdT9OuCNdsZOc0W271wk1FmRl9Rm0hmY2aA33vdTNo8UkkF5XwU6obS2zcWImF5ewO+z2wp0hzU4pBtLDK0X46N5JPmEW/UvZXfQj3T3Rkx6HunsSoEtEd8/+cbjlt87p7plFU0FWgwVHmsUwo97utID+s54sIrxI81J+h9ZMCPnXAkXUiLvsmsdHLboRLeJuHR2bVJddk9ssWV6PKELibrNoUm3mMeXO8VG/1XL6JJecRsk0HfokT4GFjG4tGcZ18y5E7c6l9IGYza6LdfYItMXKogUt8ogGt+G807Gcfv440fU6cwp1+SpGVr3nL/YvzzTurQjVOvdKBJCPrz+rUjjM9rLLjYOt3QpbmUa1GY/l4xVj7BNfY5rPvUEnY/ZdVoYRd7mFj2dyO7FbmpUTni1QRuwzFqrNOh/SxquyLn5wtHeZ861Pf+dPOkahhlSpF2nHgF5DdLUCt5G+dZn/Lax/WjGX4WAC5yodnfAZ+CKdXiHuJh0lbgh8/bbBJ3QxMUzVE3yBUJLLkLLoTx4rrwf8ezemETWulns9eJpEiRNJNleSxMmLBwNWh/ipRY07yV51B88kKVH0FtIJ5dV8eQBvBplaKj/lDWfLi/Vu+Z0UJRq6KoQ35cFzGUps/EMVwvluuSxBicbOz8oQopHou33kyBtIBOi08f7nr/OGswUT3pTLzQZGQzmT/vyXp+/exeSygMYaIUFf1l75pzqE8+Vy+e3zT0+fvSsPsJQH5Zh6CwXY+/Dh9vb2/fuXrnx6v7LwUCFCpESbLJCBmWZoGtWrlYWFlZAsLDz8NW84W2zC+TIlg+fJEQ3jIwKKyrVShDckXPemixGBpMOA56DGBwBw4YFShLYSu92bm3lHbMSnERyjYX68bTeotKlxCwFeK0YYFazUwTMSxmjUnw3QWPv4qRomb6BJBfHQogjhDzChg/jOr6AZjeYzNBVdLeAJ5fY3wlobLxmAyhA+ggkdRNdrGI3aU3uqvbINcGXl6mXPZWx8YgEqT+iMzUERe+/eL64rufZG2crKh98M/NZzJuAMEDqIb5tNj687331wfeVDXr1st5kmigm/yRvOFh6hM6UOfD70An5yQpHYsV8xAGeC0EYs+3wu4QNCkdjvzTShFwp0XUfZ9R//OhZwRggdRC8QIAg9RbIBVSH8VwwhQrwJ/qcbZrjmAc4MYUi6PKJ7wpzk23vCe8J7wtzlnvCe8J4wf7knnIbwy7zhbLknvCe8a4S/zyDh9ykI17/79W93mnD9u7m5n1IgzhwhBpybe5MccdYIH/3b+cDn37fvJuGj/3if+PwwIeJsEQaACPFBMsSZItx8RX5mWE6EOEuEYUAkfzy8W4SbL6iPJUGcHcJTGnBu7s94xJkhPP0B/ODrWMRZITz9lvHJv+KC1BkhPP2e+dEvY8Kb2SDkAMYiKkL4I5fw9Efuh7/hIs4CYQzg3Bw3m5oBwtOvYj/+NQdRfcLTNwk+z0kYlSfcTALIQ1SdcPNzwm94w0oYVSHchAEfJQVkJ4xKE66vJwdkIqpMuD6fBpCVEytMuH6TDpCRE6tL6BTVUgqQMCpLOBEglDCqSuhVDVMLlTAqSjgxII2oJiFZNUwtkZx4+y9hTzmNhAk3pwGMJowqElJVw7QSShgVJASqhmmFRFSE8KuAEKwaphUCcfu/Ar5vegkIGVXDtBLkxKoRCgIkEBUjZJZF04u3iLr9WthXTiMuIbdqmFZcRKUIY4tq6cRJGFUiFAzoIipEmKBqmFZwTrz9p/CvnUQQoQRAJOVtZQgTlUUnkD8eKkL4P0mACFENwjfSAFGqIeJL/g8uoBpwXbN9+AAAAABJRU5ErkJggg=='
        send_button_message(event.reply_token, text, btn, url)

    def on_enter_dead(self, event):
        global score
        text = f'Sorry! You LOST!\nYour score is {score} points.\nDo you want to start again?'
        btn = [
            MessageTemplateAction(
                label='yes',
                text='yes'
            ),
            MessageTemplateAction(
                label='no',
                text='no'
            ),
        ]
        url = 'https://st2.depositphotos.com/8615356/11489/v/950/depositphotos_114890456-stock-illustration-skull-vector-illustration.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_user(self, event):
        text = event.message.text
        if text == 'yes':
            is_restart = True
        return is_restart
