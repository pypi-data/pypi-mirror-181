import json
import datetime
from bai2 import bai2


def bai_to_json(bai):
    bai_dict = {}

    # first line of the bai is the file header, corresponds to 01
    bai_dict['sender_id'] = bai.header.sender_id
    bai_dict['receiver_id'] = bai.header.receiver_id
    bai_dict['creation_date'] = bai.header.creation_date.isoformat()
    bai_dict['creation_time'] = bai.header.creation_time.isoformat()
    bai_dict['file_id'] = bai.header.file_id
    bai_dict['physical_record_length'] = bai.header.physical_record_length
    bai_dict['block_size'] = bai.header.block_size
    bai_dict['version_number'] = bai.header.version_number
    bai_dict['file_control_total'] = bai.trailer.file_control_total
    bai_dict['number_of_groups'] = bai.trailer.number_of_groups
    bai_dict['number_of_records'] = bai.trailer.number_of_records
    bai_dict['groups'] = []

    for idx, group in enumerate(bai.children): # file child is the group, corresponds to 02
        group_data = {
            'idx' : idx,
            'ultimate_receiver_id': group.header.ultimate_receiver_id,
            'originator' : group.header.originator_id,
            'group_status' : group.header.group_status.name,
            'as_of_date' : group.header.as_of_date.isoformat(),
            'as_of_time' : group.header.as_of_time,
            'currency' : group.header.currency,
            'group_control_total' : group.trailer.group_control_total,
            'number_of_accounts' : group.trailer.number_of_accounts,
            'number_of_records' : group.trailer.number_of_records,
            'accounts' : []
        }

        for idx, account in enumerate(group.children): # group child is the account, 03
            account_data = {
                'idx' : idx,
                'customer_account_number' : account.header.customer_account_number,
                'customer_currency_code' : account.header.currency,
                'account_control_total' : account.trailer.account_control_total,
                'number_of_records' : account.trailer.number_of_records,
                'summaries' : [],
                'transactions' : []
            }

            for idx, summary in enumerate(account.header.summary_items): # account header contains summaries
                summary_data = {
                    'idx' : idx,
                    'type_code' : summary.type_code.description,
                    'amount' : summary.amount,
                    'item_count' : summary.item_count,
                    'funds_type' : summary.funds_type,
                }
                account_data['summaries'].append(summary_data)

            for idx, transaction in enumerate(account.children): # accont child is the transaction, 16
                transaction_data = {
                    'idx' : idx,
                    'type_code' : transaction.type_code.description,
                    'amount' : transaction.amount,
                    'funds_type' : transaction.funds_type,
                    'bank_reference' :  transaction.bank_reference,
                    'customer_reference' : transaction.customer_reference,
                    'text' : transaction.text
                }
                account_data['transactions'].append(transaction_data)

            group_data['accounts'].append(account_data)

        bai_dict['groups'].append(group_data)

    bai_json = json.dumps(bai_dict, indent=4)
    return bai_json

def file_to_json(path):
    with open(path) as f:
        bai = bai2.parse_from_file(f)
        return bai_to_json(bai)

def string_to_json(string):
    bai = bai2.parse_from_string(string)
    return bai_to_json(bai)
