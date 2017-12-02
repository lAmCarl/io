<html>
<head>
<link rel="stylesheet" type="text/css" href="query_style.css">

<style>
  .center {
    display: inline-block;
    width: 80%;
    padding: 50px 0px;
    text-align: left;
  }
</style>
</head>
<body>

<!-- Colour-blocked logo, search bar and sign-in/sign-out button -->
<div class="bar">
  <div class="left">
    <a href="/">
      <img src="cow.png" alt="Cow Logo" title="Return to homepage" align="left" width="118" height="164" style="padding-right:20px;"> </a>
    <div class="center">
      <form action="/" method="get"> <input name="keywords" type="text" placeholder="Search..."/> 
            <input value="Submit" type="submit" /> </form>
    </div>
  </div>
</div>
<br>
<!-- Search results, 5 URLs per page -->
<div class="left">
  <h3> Search for "<i>{{query}}</i>" </h3>

  % if len(docs) == 0:
    <p> No results found. </p>
  <% else:
    for link in docs:
  %>
      <p><a href={{link}}>{{link}}</a></p>
  %   end
  % end
  <!-- Word count and search history -->
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

  <%
<!-- Page navigation -->
  <div class="pagination">
    <%
    num_pages = zlen/5
    if zlen % 5:
      num_pages += 1
    end
    if page > 1:
      link = url + "&page=" + str(page-1)
    %>
    <a href={{link}}>&laquo; <span>Previous</span></a>
    % end
    <% for i in range(1,num_pages+1):
      link = url + "&page=" + str(i)
      if i == page:
    %>
        <a class="active" href={{link}}>{{i}}</a>
      % else:
        <a href={{link}}>{{i}}</a>
      % end
    % end
    <% if page < num_pages:
        link = url + "&page=" + str(page+1)
    %>
      <a href={{link}}> <span>Next</span> &raquo; </a>
    % end
  </div>
</div>
</body>
</html>
