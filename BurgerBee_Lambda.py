import json

burger_sizes = ['single', 'double', 'triple']
burger_franchises = ['burger king', 'habbit burger', 'mc donald']
best_burger_types = ['plain', 'cheese', 'bacon']
burger_palace_types = ['egg', 'pickle', 'tomatoe']
flaming_burger_types = ['chilli', 'jalapeno', 'peppercorn']


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
            'invalidSlot': 'BurgerType'
        }

    # Validate BurgerType for BurgerFranchise
    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'burger king':
        if slots['BurgerType']['value']['originalValue'].lower() not in best_burger_types:
            print('Invalid BurgerType for burger king')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'message': 'Would you like to add? {}.'.format(", ".join(best_burger_types))
            }

    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'mc donald':
        if slots['BurgerType']['value']['originalValue'].lower() not in burger_palace_types:
            print('Invalid BurgerType for mc donald')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'message': 'Would you like to add? {}.'.format(", ".join(burger_palace_types))
            }

    if slots['BurgerFranchise']['value']['originalValue'].lower() == 'habbit burger':
        if slots['BurgerType']['value']['originalValue'].lower() not in flaming_burger_types:
            print('Invalid BurgerType for habbit burger')

            return {
                'isValid': False,
                'invalidSlot': 'BurgerType',
                'message': 'Would you like to add? {}.'.format(", ".join(flaming_burger_types))
            }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
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
                    "content": "Yey! Your order is confirmed."
                }
            ]
        }

    print(response)
    return response