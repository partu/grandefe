from jinja2 import Template



players_template = Template('''
<link href='style.css' rel='stylesheet' type='text/css'>

<table cellspacing='0'> <!-- cellspacing='0' is important, must stay -->
  <thead>
    <tr>
      <th>Nombre</th>
      <th>Posicion</th>
      <th>Categoria</th>
    </tr>
  </thead>


  <tbody>
  {% for player in players %}
    <tr>
      <td> {{player.name}}  </td>
      <td> {{player.position}}  </td>
      <td> {{player.category}}  </td>
    </tr>
  {% endfor %}
  </tbody>

</table>
''')




teams_template = Template('''
<link href='style.css' rel='stylesheet' type='text/css'>

<table cellspacing='0'> <!-- cellspacing='0' is important, must stay -->
  <thead>
    <tr>
      <th>Dni</th>
      <th>Usuario</th>
      <th>Nombre equipo</th>
      <th>Titulares</th>
      <th>Suplentes</th>
    </tr>
  </thead>


  <tbody>
  {% for team in teams %}
    <tr>
      <td> {{team.key[0]}}  </td>
      <td> {{team.key[1]}}  </td>
      <td> {{team.key[2]}}  </td>
      <td> {{", ".join(team.titulars)}}  </td>
      <td> {{", ".join(team.alternates)}}  </td>
    </tr>
  {% endfor %}
  </tbody>

</table>
''')


teams_points_template = Template('''
<link href='style.css' rel='stylesheet' type='text/css'>

<table cellspacing='0'> <!-- cellspacing='0' is important, must stay -->
  <thead>
    <tr>
      <th>Dni</th>
      <th>Nombre usuario</th>
      <th>Nombre equipo</th>
      {% for i in range(1,rounds+1) %}
      <th> Fecha {{i}}</th>
      {% endfor %}
      <th> Total </th>
    </tr>
  </thead>


  <tbody>
  {% for team in teams_points %}
    <tr>
      <td> {{team[0][0]}}  </td>
      <td> {{team[0][1]}}  </td>
      <td> {{team[0][2]}}  </td>
      {% for round, points in team[1] %}
      <td>  {{points}}  </td>
      {% endfor %}
    </tr>
  {% endfor %}
  </tbody>

</table>
''')

player_points_template = Template('''
<link href='style.css' rel='stylesheet' type='text/css'>

<table cellspacing='0'> <!-- cellspacing='0' is important, must stay -->
  <thead>
    <p1> Nombre: {{player.name}} </p1><br>
    <p2> Posicion: {{player.position}} </p2><br>
    <p3> Categoria: {{player.category}} </p3><br>

    <tr>
      {% for i in range(1,rounds+1) %}
      <th> Fecha {{i}}</th>
      {% endfor %}
      <th> Total </th>
    </tr>
  </thead>


  <tbody>
    <tr>
      {% for round, points in player_points %}
      <td>  {{points}}  </td>
      {% endfor %}
    </tr>
  </tbody>

</table>
''')