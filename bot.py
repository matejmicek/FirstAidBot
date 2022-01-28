#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

'''
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
'''


import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

import time


READY_TEXT = 'Ready'
NOT_READY_TEXT = 'Give me a break'
BETTER_TEXT = 'Yes, they are better'
NOT_BETTER_TEXT = 'No, I still need help'


# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger(__name__)

AREA_DECISION, READY, BETTER, TEST_STATE = range(4)


keyboard_to_action = [
    'Bleeding',
    'Fracture',
    'Hear Failure',
    #'Other': OTHER_PROBLEM,
]


def my_new_state(update: Update, context: CallbackContext):
    logger.info('in my new state')
    logger.info(update.message.text)


READY_KEYBOARD = ReplyKeyboardMarkup(
            [[READY_TEXT], [NOT_READY_TEXT]],
            one_time_keyboard = True,
            input_field_placeholder = 'Are you ready to start?',
        )
    
    
IS_PATIENT_BETTER_KEYBOARD= ReplyKeyboardMarkup(
            [[BETTER_TEXT], [NOT_BETTER_TEXT]],
            one_time_keyboard = True,
            input_field_placeholder = 'Is the patient better now?',
        )



TOKEN = '5258655199:AAHiI4wKd-lDGfodAV3pMiHpxpehnxNVwlk'


def chunks(lst, n):
    ''' Yield successive n-sized chunks from lst. '''
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def start(update: Update, context: CallbackContext):
    reply_keyboard = chunks(keyboard_to_action, 2)

    update.message.reply_text(
        '''First Aid Bot to your rescue ...
What happened?
        ''',
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard = True,
            input_field_placeholder = 'What happened?',
        )
    )
    return AREA_DECISION


def area_decision(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    logger.info('area_decision %s: %s', user.first_name, text)
    update.message.reply_text(
        f'I see! Let me have a look what can I do with {text}',
        reply_markup = ReplyKeyboardRemove(),
    )

    return emergency_handlers[text](update, context)


def handle_heart_failure(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    logger.info('handle_heart_failure %s: %s', user.first_name, text)
    update.message.reply_text(
        f'Now, here are instructions for dealing with heart fauilure',
        reply_markup = ReplyKeyboardRemove(),
    )
    time.sleep(1)
    update.message.reply_photo(open('resuscitation.jpg', 'rb'))
    time.sleep(1)
    update.message.reply_text(
        f'You will perform resuscitation, place the patient on their back and place your hands as shown in the picture. Let me know when you are ready.',
        reply_markup = READY_KEYBOARD
    )
    
    context.user_data['next_step'] = resuscitation
    logger.info('Returning READY from handle heart failure')
    return READY




def handle_broken(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    logger.info('handle_broken %s: %s', user.first_name, text)
    
    update.message.reply_text(
        f'Now, here are instructions for dealing with a fracture. Let me know when you are ready.',
        reply_markup = READY_KEYBOARD,
    )

    context.user_data['next_step'] = broken
    return READY

def handle_bleeding(update: Update, context: CallbackContext):
    user = update.message.from_user
    text = update.message.text
    logger.info('handle_bleeding %s: %s', user.first_name, text)
    
    update.message.reply_text(
        f'Now, here are instructions for dealing with bleeding. Let me know when you are ready.',
        reply_markup = READY_KEYBOARD,
    )

    context.user_data['next_step'] = bleeding
    return READY




def bleeding(update: Update, context: CallbackContext):
   
    update.message.reply_photo(open('bleeding.jpeg', 'rb'))
    time.sleep(1)
    update.message.reply_text(
        'Try to stop the beeding by pressing hard with a cloth at the affected area as shown in the picture.',
        reply_markup = ReplyKeyboardRemove()
    )
    time.sleep(1)
 
    update.message.reply_text(
        f'Start wrapping the injured area with other pieces of cloth, do this as long as bleeding continues.',
        reply_markup = IS_PATIENT_BETTER_KEYBOARD
    )
    
    context.user_data['more'] = bleeding_more
    return BETTER




def bleeding_more(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Try using your belt to secure the area even tighter.',
        reply_markup = ReplyKeyboardRemove()
    )
 
    return end(update, context)





def broken(update: Update, context: CallbackContext):
   
    update.message.reply_photo(open('broken.jpg', 'rb'))
    time.sleep(1)
    update.message.reply_text(
        'Place a hard object at the area of injury, this can be a wooden stick or a piece of metal.',
        reply_markup = ReplyKeyboardRemove()
    )
    time.sleep(1)
 
    update.message.reply_text(
        f'Wrap the part of the body and the object together so that it is fixed. Escort the person to the hospital while trying to not to move with the injured part.',
        reply_markup = IS_PATIENT_BETTER_KEYBOARD
    )
    
    context.user_data['more'] = broken_more
    return BETTER



def broken_more(update: Update, context: CallbackContext):
       
    update.message.reply_text(
        'You can give the patient painkillers, this might help transfering them to the hospital.',
        reply_markup = ReplyKeyboardRemove()
    )
 
    return end(update, context)



def resuscitation(update: Update, context: CallbackContext):
    logger.info('in resuscitation')
    update.message.reply_text(
        f'Press in the rythm that I will provide by sending messages',
        reply_markup = ReplyKeyboardRemove(),
    )
    time.sleep(2)
    
    for _ in range(10):
        update.message.reply_text(
            f'Push',
            reply_markup = ReplyKeyboardRemove(),
        )
        time.sleep(1)
        
    update.message.reply_text(
            f'Is the patient better now?',
            reply_markup = IS_PATIENT_BETTER_KEYBOARD,
        )
    logger.info('Returning BETTER from resuscitation')
    context.user_data['more'] = resuscitation_more
    return BETTER




def resuscitation_more(update: Update, context: CallbackContext):
    logger.info('in resuscitation')
    update.message.reply_text(
        f'Continue pressing in this rythm. If the patient does not get better, try breathing into their lungs.',
        reply_markup = ReplyKeyboardRemove(),
    )
    time.sleep(2)
    
    for _ in range(10):
        update.message.reply_text(
            f'Push',
            reply_markup = ReplyKeyboardRemove(),
        )
        time.sleep(1)
        
    update.message.reply_text(
            f'Is the patient better now?',
            reply_markup = IS_PATIENT_BETTER_KEYBOARD,
        )
    
    logger.info('Returning BETTER from resuscitation')
    return BETTER


def better(update: Update, context: CallbackContext):
    logger.info('in better')
    text = update.message.text
    if text == BETTER_TEXT:
        update.message.reply_text(
            f'Very nice!',
            reply_markup = ReplyKeyboardRemove(),
        )
        return end(update, context)
        
    elif text == NOT_BETTER_TEXT:
        if 'more' in context.user_data:
            res = context.user_data['more'](update, context)
            del context.user_data['more']
            return res
        else:
            update.message.reply_text(
                f'Seems like you need more help... I did my best, try calling Emergency.',
                reply_markup = ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
    else:
        raise RuntimeError(f'unknown text: {text} received in better') 


def ready_to_start(update: Update, context: CallbackContext):
    logger.info('in ready to start')
    text = update.message.text
    if text == READY_TEXT:
        logger.info('Going for the next step ')
        return context.user_data['next_step'](update, context)
    elif text == NOT_READY_TEXT:
        logger.info('person not ready')
        update.message.reply_text(
            f'Ok, I will wait for a bit.',
            reply_markup = READY_KEYBOARD
        )
        return READY
    else:
        raise RuntimeError(f'unknown text: {text} received `in ready to start`') 



def end(update: Update, context: CallbackContext):
    logger.info('in end')
    update.message.reply_text(
        f'Thank you for using First Aid Bot! If there are any more problems, call Emergency',
        reply_markup = ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    ''' Cancels and ends the conversation. '''
    user = update.message.from_user
    logger.info('User %s canceled the conversation.', user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup = ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    ''' Run the bot. '''
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            AREA_DECISION: [MessageHandler(Filters.text, area_decision)],
            READY: [MessageHandler(Filters.text, ready_to_start)],
            BETTER: [MessageHandler(Filters.text, better)],
            TEST_STATE: [MessageHandler(Filters.text, my_new_state)],
        },
        fallbacks = [CommandHandler('cancel', cancel), CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
 

emergency_handlers = {
    'Hear Failure': handle_heart_failure,
    'Fracture': handle_broken,
    'Bleeding': handle_bleeding
}


if __name__ == '__main__':
    main()
