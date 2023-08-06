# social-stats 

## Installation

```shell
pip install social-stats
```

## Example
```python
import socialstats

data = socialstats.get_stat(platform='codechef', username='sudiptob2')
print(data)
```
```shell
{'username': 'sudiptob2', 'first_name': 'sudipto baral', 'avatar_url': 'https://cdn.codechef.com/sites/default/files/uploads/pictures/eb7dbb909bbcc5999fdbb9377722b615.jpg', 'star': '2', 'rating': '1523', 'highest_rating': '1562', 'motto': 'Learning code', 'profession': 'Student', 'country': 'Bangladesh', 'org': 'Patuakhali Science And technology University ', 'solved': '33', 'authored': '0', 'tested': '0', 'contributed': '0'}

```