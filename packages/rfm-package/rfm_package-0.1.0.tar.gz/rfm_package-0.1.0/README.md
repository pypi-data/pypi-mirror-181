
# RFM Package

A Python package for Recency, Frequency, Monetary model (RFM), which is an analysis is a behavior based technique used
to segment customers by examining their transaction history.

* how recently a customer has purchased (Recency)
* how often they purchase (Frequency)
* how much the customer spends (Monetary)


## License

* Free software: MIT license
* Documentation: https://rfm-package.readthedocs.io.

## Installation
You can install the package using
```
pip install rfm_package

```

## Usage Test

```
orders = pd.read_csv(r'C:/Users/Admin/Desktop/RFM-Package/rfm_package/data/orders.csv', parse_dates = ['order_date'])

columns = create_rfm_columns(orders, "customer_id", "order_date", "revenue")
print(columns)

scaled = scale_rfm_columns(columns)
print(scaled)

plot_rfm(scaled)

scores = rfm_scores(scaled)
print(rfm_scores(scaled))

named_segments = give_names_to_segments(scores)
print(named_segments)

dist = segments_distribution(named_segments)
print(dist)

visualize_segments(dist)

```

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
