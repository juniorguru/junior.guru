# SUBSCRIPTIONS_GQL_PATH = Path(__file__).parent / 'subscriptions.gql'

# COUPON_NAMES_CATEGORIES_MAPPING = {
#     'THANKYOU': ClubSubscribedPeriodCategory.FREE,
#     'THANKYOUFOREVER': ClubSubscribedPeriodCategory.FREE,
#     'THANKYOUTEAM': ClubSubscribedPeriodCategory.TEAM,
#     'PATREON': ClubSubscribedPeriodCategory.FREE,
#     'GITHUB': ClubSubscribedPeriodCategory.FREE,
#     'FOUNDERS': ClubSubscribedPeriodCategory.FREE,
#     'FINAID': ClubSubscribedPeriodCategory.FINAID,
#     'CORESKILL': ClubSubscribedPeriodCategory.CORESKILL,
#     'STUDENTCORESKILL': ClubSubscribedPeriodCategory.CORESKILL,
# }


# ClubSubscribedPeriod.drop_table()
# ClubSubscribedPeriod.create_table()

# logger.info('Mapping coupons to categories')
# coupon_names_categories_mapping = {
#     **{parse_coupon(coupon)['name']: ClubSubscribedPeriodCategory.PARTNER
#        for coupon in Partner.coupons()},
#     **{parse_coupon(coupon)['name']: ClubSubscribedPeriodCategory.STUDENT
#        for coupon in Partner.student_coupons()},
#     **COUPON_NAMES_CATEGORIES_MAPPING
# }


# subscriptions = list(memberful.get_nodes(SUBSCRIPTIONS_GQL_PATH.read_text()))
# print(len(subscriptions))
# print(len(set([s['member']['id'] for s in subscriptions if s['active']])))


#     for subscribed_period in get_subscribed_periods(subscription):
#         if subscribed_period['coupon']:
#             coupon_name = parse_coupon(subscribed_period['coupon'])['name']
#             category = coupon_names_categories_mapping.get(coupon_name, ClubSubscribedPeriodCategory.INDIVIDUALS)
#         elif subscribed_period['is_trial']:
#             category = ClubSubscribedPeriodCategory.TRIAL
#         else:
#             category = ClubSubscribedPeriodCategory.INDIVIDUALS
#         ClubSubscribedPeriod.create(account_id=account_id,
#                                     start_on=subscribed_period['start_on'],
#                                     end_on=subscribed_period['end_on'],
#                                     interval_unit=subscription['plan']['intervalUnit'],
#                                     has_feminine_name=has_feminine_name,
#                                     category=category)


# def get_subscribed_periods(subscription):
#     orders = list(sorted(subscription['orders'], key=itemgetter('createdAt'), reverse=True))
#     renewal_on = arrow.get(subscription['expiresAt']).date()

#     if subscription.get('trialStartAt') and subscription.get('trialEndAt'):
#         trial = (arrow.get(subscription['trialStartAt']).date(),
#                  arrow.get(subscription['trialEndAt']).date() - timedelta(days=1))
#     else:
#         trial = None

#     for i, order in enumerate(orders):
#         start_on = arrow.get(order['createdAt']).date()
#         end_on = renewal_on - timedelta(days=1)
#         is_trial = ((start_on, end_on) == trial) if trial else False

#         if subscription['coupon'] and i == 0:
#             coupon = subscription['coupon']
#         else:
#             coupon = order['coupon']
#         coupon = (coupon or {}).get('code')

#         yield dict(start_on=start_on, end_on=end_on, is_trial=is_trial, coupon=coupon)
#         renewal_on = start_on


# def format_date(value):
#     return f'{value:%Y-%m-%d}' if value else None
