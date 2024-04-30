import json

burger_sizes = ['single', 'double', 'triple']
burger_franchises = ['burger king', 'habbit burger', 'mc donald']
burger_king_types = ['plain', 'cheese', 'bacon']
habbit_burger_types = ['egg', 'pickle', 'tomatoe']
mc_donald_types = ['chili', 'jalapeno', 'peppercorn']


def validate_order(slots):
    # Validate BurgerSize
    if not slots['BurgerSize']:
        print('Validating BurgerSize Slot')

        return {
            'isValid': False,
            'invalidSlot': 'BurgerSize'
        }

    if slots['BurgerSize']['value']['originalValue'].lower() not in burger_sizes:
        print('Invalid BurgerSize')

        return {
            'isValid': False,
            'invalidSlot': 'BurgerSize',
            'message': 'Please select a {} burger size.'.format(", ".join(burger_sizes))
        }

    # Validate BurgerFranchise
    if not slots['BurgerFranchise']:
        print('Validating BurgerFranchise Slot')

        return {
            'isValid': False,
            'invalidSlot': 'BurgerFranchise'
        }

    if slots['BurgerFranchise']['value']['originalValue'].lower() not in burger_franchises:
        print('Invalid BurgerSize')

        return {
            'isValid': False,
            'invalidSlot': 'BurgerFranchise',
            'message': 'Please select from {} burger franchises.'.format(", ".join(burger_franchises))
        }

    # Validate BurgerType
    if not slots['BurgerType']:
        print('Validating BurgerType Slot')

        return {
            'isValid': False,
            'invalidSlot': 'BurgerType',
            'invalidFranchise': ''
        }

    # Validate BurgerType for BurgerFranchise
    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'burger king':
        if slots['BurgerType']['value']['originalValue'].lower() not in burger_king_types:
            print('Invalid BurgerType for burger king')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'invalidFranchise': 'burger_king',
                'message': 'Please select a burger king type of {}.'.format(", ".join(burger_king_types))
            }

    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'habbit burger':
        if slots['BurgerType']['value']['originalValue'].lower() not in habbit_burger_types:
            print('Invalid BurgerType for habbit burger')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'invalidFranchise': 'habbit_burger',
                'message': 'Please select a habbit burger type of {}.'.format(", ".join(habbit_burger_types))
            }

    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'mc donald':
        if slots['BurgerType']['value']['originalValue'].lower() not in mc_donald_types:
            print('Invalid BurgerType for mc donald')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'invalidFranchise': 'mc_donald',
                'message': 'Please select a mc donald type of {}.'.format(", ".join(mc_donald_types))
            }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)
    print(order_validation_result)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            response_message = 'BurgerBee'
            if 'message' in order_validation_result:
                response_message = order_validation_result['message']

            response_card_sub_title = ''
            response_card_buttons = []

            burger_king_sub_title = 'Please select a burger king type'
            burger_king_buttons = [
                {
                    "text": "Plain",
                    "value": "plain"
                },
                {
                    "text": "Cheese",
                    "value": "cheese"
                },
                {
                    "text": "Bacon",
                    "value": "bacon"
                }
            ]

            habbit_burger_sub_title = 'Please select a habbit burger type'
            habbit_burger_buttons = [
                {
                    "text": "egg",
                    "value": "egg"
                },
                {
                    "text": "pickle",
                    "value": "pickle"
                },
                {
                    "text": "tomatoe",
                    "value": "tomatoe"
                }
            ]

            mc_donald_sub_title = 'Please select a mc donald type'
            mc_donald_buttons = [
                {
                    "text": "Chili",
                    "value": "chili"
                },
                {
                    "text": "Jalapeno",
                    "value": "jalapeno"
                },
                {
                    "text": "Peppercorn",
                    "value": "peppercorn"
                }
            ]

            if order_validation_result['invalidSlot'] == "BurgerSize":
                response_card_sub_title = "Please select a Burger size"
                response_card_buttons = [
                    {
                        "text": "Single",
                        "value": "single"
                    },
                    {
                        "text": "Double",
                        "value": "double"
                    },
                    {
                        "text": "Triple",
                        "value": "triple"
                    }
                ]

            if order_validation_result['invalidSlot'] == "BurgerFranchise":
                response_card_sub_title = "Please select a Burger Franchise"
                response_card_buttons = [
                    {
                        "text": "Burger King",
                        "value": "burger king"
                    },
                    {
                        "text": "Habbit Burger",
                        "value": "habbit burger"
                    },
                    {
                        "text": "Mc Donald",
                        "value": "mc donald"
                    }
                ]

            if order_validation_result['invalidSlot'] == "BurgerType":
                if order_validation_result['invalidFranchise'] == "burger_king":
                    response_card_sub_title = burger_king_sub_title
                    response_card_buttons = burger_king_buttons
                elif order_validation_result['invalidFranchise'] == "habbit_burger":
                    response_card_sub_title = habbit_burger_sub_title
                    response_card_buttons = habbit_burger_buttons
                elif order_validation_result['invalidFranchise'] == "mc_donald":
                    response_card_sub_title = mc_donald_sub_title
                    response_card_buttons = mc_donald_buttons
                else:
                    response_card_sub_title = 'Please select a burger type'
                    response_card_buttons = [
                        {
                            "text": "Plain",
                            "value": "plain"
                        },
                        {
                            "text": "Cheese",
                            "value": "cheese"
                        },
                        {
                            "text": "Bacon",
                            "value": "bacon"
                        }
                        ,
                        {
                            "text": "pickle",
                            "value": "pickle"
                        },
                        {
                            "text": "Chili",
                            "value": "chili"
                        }
                    ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": order_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                    }
                },
                "messages": [
                    {
                        "contentType": "ImageResponseCard",
                        "content": response_message,
                        "imageResponseCard": {
                            "title": "BurgerBee",
                            "subtitle": response_card_sub_title,
                            "imageUrl": "YOUR_IMAGE_URL_HERE",
                            "buttons": response_card_buttons
                        }
                    }
                ]
            }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response