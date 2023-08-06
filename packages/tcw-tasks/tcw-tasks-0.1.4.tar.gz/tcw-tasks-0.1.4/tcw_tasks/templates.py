
TEXT_TEMPLATE = """
CONTEST EXPIRED:
  - contest name: {{ contest.title }}

STATISTICS:
  - max_entrants: {{ contest.max_entrants }}
  - number of winners: {{ contest.attributes.winners | length }}
  - sign ups: {{ contest.entrants | length }}
  - expired: {{ contest.expires.strftime('%Y-%m-%d %H:%M:%S') }} UTC

{% if contest.attributes.winners | length -%}
THE WINNERS:
  {% for winner in contest.attributes.winners -%}
  {{ loop.index }}. {{ winner }}
  {% endfor %}

It is your responsibilty to contact the winners.
Thank You!
{%- else %}
Sorry. There were no winners selected, because no one signed up.
{% endif %}

Please do not respond directly to this e-mail. The originating e-mail account is not monitored.

thecontestkitty.com
"""

HTML_TEMPLATE = """
<html>
  <head>
    <style>
      .container {
        position: relative;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
        box-sizing: border-box; }
      html {
        font-size: 62.5%; }
      body {
        font-size: 1.5em;
        line-height: 1.6;
        font-weight: 400;
        font-family: "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #222; }
      .card {
        border: 1px solid #da70d6;
        border-radius: 5px;
        padding: 1.5em; }
      footer {
        color: #999; }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <h3>Contest Expired</h3>
        <p>
        {{ contest.title }}
        </p>

        <h3>Statistics</h3>
        <div>
            <div>max entrants = {{ contest.max_entrants }}</div>
            <div>number of winners = {{ contest.attributes.winners | length }}</div>
            <div>sign-ups = {{ contest.entrants | length }}</div>
            <div>expired = {{ contest.expires.strftime('%Y-%m-%d %H:%M:%S') }} UTC</div>
        </div>

        {% if contest.attributes.winners | length %}
        <h3>The Winners</h3>
        <div class="card">
            <ol>
              {% for winner in contest.attributes.winners -%}
              <li>{{ winner }}</li>
              {% endfor %}
            </ol>
        </div>
        <footer>
            <p>
            It is your responsibilty to contact the winners.
            Please do not respond directly to this e-mail. The originating e-mail account is not monitored.
            </p>
            <p>
            <a href="https://thecontestkitty.com">thecontestkitty.com</a>
            </p>
        </footer>
        {%- else %}
        <p>Sorry. There were no winners selected, because no one signed up.</p>
        {% endif %}
      </div>
    </div>
  </body>
</html>
"""
