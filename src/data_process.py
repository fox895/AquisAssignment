import pandas as pd


def clean_type_8(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans a DataFrame which contains data from messages of type 8.
    It removes unused columns, fixes columns' type, set the correct index for
    joins, sort the dataframe, and finally renames the main columns
    """

    return (
        df.drop(['umtf', 'mic', 'tickTableId'], axis=1)
        .astype({
            'securityId': 'Int64',
            'isin': 'string',
            'currency': 'string'
        })
        .set_index('securityId')
        .sort_index()
        .rename(
            {
                'isin': 'ISIN',
                'currency': 'Currency'
            }, axis=1)
        )


def aggregate_type_12(df: pd.DataFrame) -> pd.DataFrame:
    """
    This functions generate all the aggregated data from a Dataframe containing
    messages of type 12.
    The aggregation function are very similar one another one could think of creating
    a generic function that can return all of those type of results.
    This may not be convenient and easy to read.
    """


    # Recast into proper types
    df = df.astype({
        'securityId': 'Int64',
        'side': 'category',
        'quantity': 'Int64',
        'price': 'Int64',
        'orderId': 'Int64',
    })

    # Drop duplicate rows, keep first encounter
    df = df.drop_duplicates(keep='last')

    # Generate weighted price
    df['weighted_price'] = (df['price']/df['quantity'])

    # Generate groupedBy dataframe
    df_grouped_by = df.groupby(['securityId', 'side'])

    #  Generated total quantities
    df_quantities = (
        df_grouped_by.sum()
        .loc[:, 'quantity']
        .unstack(level=-1)
        .rename(
            {
                'BUY': 'Total Buy Quantity',
                'SELL': 'Total Sell Quantity'
            }, axis=1)
    )

    # Generate total counts
    df_counts = (
        df_grouped_by.count()
        .loc[:, 'quantity']
        .unstack(level=-1)
        .rename(
            {
                'BUY': 'Total Buy Count',
                'SELL': 'Total Sell Count'
            }, axis=1)
    )

    # Generate average weighted prices
    df_average = (
        df_grouped_by.mean()
        .loc[:, 'weighted_price']
        .unstack()
        .rename({
            'BUY': 'Weighted Average Buy Price',
            'SELL': 'Weighted Average Sell Price'
            }, axis=1
        )
    )

    # Extract Max Buy price
    df_max = (
        df_grouped_by.max()
        .loc[:, 'price']
        .unstack(level=-1)
        .loc[:, 'BUY']
        .rename('Max Buy Price')
    )

    # Extract Min Sell Price
    df_min = (
        df_grouped_by.min()
        .loc[:, 'price']
        .unstack(level=-1)
        .loc[:, 'SELL']
        .rename('Min Sell Price')
    )

    return pd.concat(
        [
            df_counts, df_quantities, df_average, df_max, df_min
        ], axis=1
    )
