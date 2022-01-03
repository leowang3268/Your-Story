from logging import fatal
from os import truncate
from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message
from linebot.models import MessageTemplateAction

# global variable
to_jail = False
to_backdoor = False
leave_backdoor = False
to_kitchen = False
to_hall = False
explore_kitchen = False
complete_explore_kitchen = False
leave_kitchen = False
to_sword_room = False
leave_sword_room = False
to_armor_room = False
to_bedroom = False
have_key = False
explore_bedroom = False
complete_explore_bedroom = False
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
    def on_enter_user(self, event):
        # initialize global variables
        global is_dead, is_win, is_restart, score, have_armor, have_key, have_sword
        is_dead = False
        is_win = False
        is_restart = False
        have_sword = False
        have_armor = False
        have_key = False
        score = 0

        text = 'Welcome to \"your story\". Type \"start game\" to start the game.'
        send_text_message(event.reply_token, text)

    def is_going_to_jail(self, event):
        global to_jail, leave_kitchen, leave_backdoor
        to_jail = False
        text = event.message.text
        if text.lower() == "start game" or text.lower() == 'leave' or leave_kitchen or leave_backdoor:
            to_jail = True
        return to_jail

    def on_enter_jail(self, event):
        global leave_kitchen, leave_backdoor
        leave_kitchen = False
        leave_backdoor = False
        text = 'which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='backdoor',
                text='backdoor'
            ),
            MessageTemplateAction(
                label='kitchen',
                text='kitchen'
            ),
            MessageTemplateAction(
                label='hall',
                text='hall'
            ),
        ]
        url = 'https://static.vecteezy.com/system/resources/thumbnails/001/312/495/small/jail-and-prison-cell-background-free-vector.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_backdoor(self, event):
        global to_backdoor
        to_backdoor = False
        text = event.message.text
        if text.lower() == 'backdoor':
            to_backdoor = True
        return to_backdoor

    def is_going_to_kitchen(self, event):
        global to_kitchen, complete_explore_kitchen
        to_kitchen = False
        text = event.message.text
        if text.lower() == 'kitchen' or complete_explore_kitchen:
            to_kitchen = True
        complete_explore_kitchen = False
        return to_kitchen

    def is_going_to_hall(self, event):
        global to_hall, leave_bedroom, leave_sword_room
        to_hall = False
        text = event.message.text
        if (text.lower() == 'hall' or text.lower() == 'leave' or leave_sword_room or leave_bedroom):
            to_hall = True
        return to_hall

    def on_enter_backdoor(self, event):
        global leave_backdoor
        text = 'The door is locked! Return to jail'
        leave_backdoor = True
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

    def is_going_to_explore_kitchen(self, event):
        global explore_kitchen
        explore_kitchen = False
        text = event.message.text
        if text.lower() == 'explore':
            explore_kitchen = True
        return explore_kitchen

    def on_enter_explore_kitchen(self, event):

        global score, complete_explore_kitchen, explore_kitchen
        explore_kitchen = False
        text = 'You\'ve found a lobster! 50 points get!'
        complete_explore_kitchen = True
        score += 50
        # url = 'https://st2.depositphotos.com/1713003/47492/v/950/depositphotos_474928178-stock-illustration-red-lobster-vector-illustration.jpg'
        send_text_message(event.reply_token, text)

    # def is_leaving_kitchen(self, event):
    #     global leave_kitchen
    #     text = event.message.text
    #     if text == 'leave':
    #         leave_kitchen = True
    #     return leave_kitchen

    def on_enter_hall(self, event):
        global leave_bedroom, leave_sword_room
        leave_bedroom = False
        leave_sword_room = False
        text = 'You\'ve entered the hall. Which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='sword room',
                text='sword room'
            ),
            MessageTemplateAction(
                label='armor room',
                text='armor room'
            ),
            MessageTemplateAction(
                label='bedroom',
                text='bedroom'
            ),
        ]
        url = 'https://media.istockphoto.com/vectors/vector-old-hall-room-with-stairs-doors-and-a-window-cartoon-vector-id1256874566?k=20&m=1256874566&s=170667a&w=0&h=NMclArE3rh9teJRgWPS-ng8LlShu1rlzNJknnRvGLI8='
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_sword_room(self, event):
        global to_sword_room
        to_sword_room = False
        text = event.message.text
        if text.lower() == 'sword room':
            to_sword_room = True
        return to_sword_room

    def is_going_to_armor_room(self, event):
        global to_armor_room
        to_armor_room = False
        text = event.message.text
        if text.lower() == 'armor room':
            to_armor_room = True
        return to_armor_room

    def is_going_to_bedroom(self, event):
        global to_bedroom, complete_explore_bedroom
        to_bedroom = False
        text = event.message.text
        if text.lower() == 'bedroom' or complete_explore_bedroom:
            to_bedroom = True
        complete_explore_bedroom = False
        return to_bedroom

    def on_enter_sword_room(self, event):
        global have_key, leave_sword_room
        leave_sword_room = False
        if not have_key:
            text = 'The room is locked.'
            leave_sword_room = True
            send_text_message(event.reply_token, text)
        else:
            global score
            text = 'You\'ve entered the sword room'
            # text = 'You\'ve entered the sword room and found a sword there. 100 points get!\nHowever, the monster is waken up by the noise and it\'s now at the outside of the sword room.\nYou need to find another way out, and QUICK!'
            score += 100
            btn = [
                MessageTemplateAction(
                    label='jump outside',
                    text='outside'
                ),
                MessageTemplateAction(
                    label='secret passage',
                    # label='At the corner of the wall, some stones are cracking. Ah-ha! There\'s a secret passage',
                    text='secret room'
                ),
            ]
            url = 'https://previews.123rf.com/images/klyaksun/klyaksun1907/klyaksun190700278/128801904-museum-exhibition-room-cartoon-vector-illustration-palace-interior-art-gallery-of-medieval-castle-em.jpg'
            send_button_message(event.reply_token, text, btn, url)

    def on_enter_armor_room(self, event):
        global score
        text = 'You\'ve entered the armor room '
        # text = 'You\'ve entered the armor room and found an armor there. 50 points get!\nHowever, the monster is waken up by the noise and it\'s now at the outside of the armor room.\nYou need to find another way out, and QUICK!'
        score += 50
        btn = [
            MessageTemplateAction(
                label='jump outside',
                text='outside'
            ),
            MessageTemplateAction(
                label='secret passage',
                # label='At the corner of the wall, some stones are cracking. Ah-ha! There\'s a secret passage',
                text='secret room'
            ),
        ]
        url = 'https://image.freepik.com/free-vector/medieval-castle-throne-room-ballroom-interior-with-knights-armor-both-sides-king_33099-892.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def on_enter_bedroom(self, event):
        text = 'You\'ve entered the monster\'s bedroom.'
        # text = 'You\'ve entered the monster\'s bedroom.\nIt is asleep now. BE QUIET!\nWhat do you want to do?'
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
        explore_bedroom = False
        text = event.message.text
        if text == 'explore':
            explore_bedroom = True
        return explore_bedroom

    def on_enter_explore_bedroom(self, event):
        global have_key, complete_explore_bedroom
        text = 'You\'ve found a key!'
        # text = 'You\'ve found a key! Who knows what is the key for?'
        complete_explore_bedroom = True
        have_key = True
        # url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQk3zCxojxTkYRzk46Row09wFEv9qK0UkbYKw&usqp=CAU'
        send_text_message(event.reply_token, text)

    # def is_leaving_bedroom(self, event):
    #     global leave_bedroom
    #     text = event.message.text
    #     if text == 'leave':
    #         leave_bedroom = True
    #     return leave_bedroom

    def is_going_to_secret_room(self, event):
        global to_secret_room
        to_secret_room = False
        text = event.message.text
        if text == 'secret room':
            to_secret_room = True
        return to_secret_room

    def on_enter_secret_room(self, event):
        text = 'In the secret room lies a box. Find the different one.'
        # text = 'You\'ve found a secret room. there\'s three boxes at front.\nFind the different one among the three. (Hint: Jay Chou)'
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
        wrong_answer = False
        text = event.message.text
        if text == '黑色毛衣' or text == '黑色幽默':
            wrong_answer = True
        return wrong_answer

    def is_going_to_correct_answer(self, event):
        global correct_answer
        correct_answer = False
        text = event.message.text
        if text == '黑色柳丁':
            correct_answer = True
        return correct_answer

    def on_enter_wrong_answer(self, event):
        global is_dead
        is_dead = True
        text = 'Oh No! You made the wrong answer and triggered the trap'
        # url = 'https://st2.depositphotos.com/4464609/6699/v/950/depositphotos_66998681-stock-illustration-guillotine.jpg'
        send_text_message(event.reply_token, text)

    def on_enter_correct_answer(self, event):
        global score
        score += 250
        text = 'Nice Job! You make the right answer and open the box.'
        # text = 'Nice Job! You make the right answer and open the box.\nThere\'s a diamond in the box. 250 points get!'
        # url = 'https://st2.depositphotos.com/1192512/7466/v/380/depositphotos_74660431-stock-illustration-golden-chain-necklace-with-heart.jpg?forcejpeg=true'
        send_text_message(event.reply_token, text)

    def is_going_to_outside(self, event):
        global to_outside
        global correct_answer
        to_outside = False
        text = event.message.text
        if text == 'outside' or correct_answer:
            to_outside = True
        return to_outside

    def on_enter_outside(self, event):
        text = 'You\'ve reached outside. Which way do you want to go?'
        btn = [
            MessageTemplateAction(
                label='lawn',
                text='lawn'
            ),
            MessageTemplateAction(
                label='gate',
                text='gate'
            ),
            MessageTemplateAction(
                label='warehouse',
                text='warehouse'
            ),
        ]
        url = 'https://static.vecteezy.com/system/resources/thumbnails/000/097/801/small_2x/keep-off-the-grass-background-free-vector.png'
        send_button_message(event.reply_token, text, btn, url)

    def is_going_to_lawn(self, event):
        global to_lawn
        to_lawn = False
        text = event.message.text
        if text == "lawn":
            to_lawn = True
        return to_lawn

    def is_going_to_gate(self, event):
        global to_gate
        to_gate = False
        text = event.message.text
        if text == "gate":
            to_gate = True
        return to_gate

    def is_going_to_warehouse(self, event):
        global to_warehouse
        to_warehouse = False
        text = event.message.text
        if text == "warehouse":
            to_warehouse = True
        return to_warehouse

    def on_enter_lawn(self, event):
        global have_armor
        global is_dead
        global is_win
        is_dead = False
        is_win = False
        if not have_armor:
            text = 'OUCH! There are traps in the lawn.'
            is_dead = True
            send_text_message(event.reply_token, text)
        else:
            text = 'You crouched in the lawn'
            # text = 'You crouched in the lawn with your armor protecting you from the traps in the lawn, and finally escaped the house.'
            is_win = True
            # url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkjRCKcJSWeqkJCqeO2vpIClwOGUtjQTg_mw&usqp=CAU'
            send_text_message(event.reply_token, text)

    def on_enter_gate(self, event):
        global have_sword
        global is_dead
        global is_win
        is_dead = False
        is_win = False
        if not have_sword:
            text = 'There\'s a guard in front of the gate.'
            # text = 'There\'s a guard in front of the gate. You have no weapon to fight him.'
            is_dead = True
            send_text_message(event.reply_token, text)
        else:
            text = 'You use your sword to defeat the guard'
            # text = 'You use your sword to defeat the guard blocking the gate, and finally escaped the house.'
            is_win = True
            # url = 'https://en.pimg.jp/079/061/259/1/79061259.jpg'
            send_text_message(event.reply_token, text)

    def on_enter_warehouse(self, event):
        global is_win
        text = 'You entered the warehouse and find a car'
        # text = 'You entered the warehouse and find a car there. You use the key stolen from the bedroom, and finally escaped the house.'
        is_win = True
        # url = 'data:image/png;base64,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'
        send_text_message(event.reply_token, text)

    def is_going_to_dead(self, event):
        return is_dead

    def is_going_to_win(self, event):
        return is_win

    def on_enter_win(self, event):
        global score
        text = f'WON!\nYour score is {score}.\nStart again?'
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
        url = 'https://previews.123rf.com/images/nezezon/nezezon1110/nezezon111000031/10799919-.jpg'
        send_button_message(event.reply_token, text, btn, url)

    def on_enter_dead(self, event):
        global score
        text = f'LOST!\nYour score is {score}.\nStart again?'
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
        global is_restart
        is_restart = False
        text = event.message.text
        if text == 'yes':
            is_restart = True
        return is_restart
