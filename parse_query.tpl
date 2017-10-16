<html>
<head>
<style>
	th, td {
		padding: 10px;
	}
</style>
</head>
<body>

<img src="cow.jpg">
<img src="name.png">

<h3> Results: </h3>

<p> Search for "<i>{{query}}</i>" </p>

<table id="results">
  <tr>
    <th><b>Word</b></th>
    <th><b>Count</b></th>
  </tr>

<%

for word, count in word_count.items():
%>
  <tr>
	<td>{{word}}</td>
    <td>{{count}}</td>
  </tr>
  % end
</table>
</body>
</html>