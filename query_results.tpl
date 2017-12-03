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
      <form action="/" method="get"> <input name="keywords" type="text" value="{{query}}"/> 
            <input value="Submit" type="submit" /> </form>
    </div>
  </div>
</div>
<br>
<!-- Search results, 5 URLs per page -->
<div class="left">
  <% if any([i[1] for i in corrected]): 
      correct = '+'.join([i[0] for i in corrected])%>
      % incorrect = query.replace(' ', '+')
    <p> Did you mean <a href="/?keywords={{correct}}">
    <% for w,c in corrected:
      if c:%>
      <b><i>{{w}}</i></b>
      <% else: %>
        {{w}} 
    <% end
    end %>
    </a>?
    <!--<br>
    Search instead for <a href="/?keywords={{incorrect}}&page=1">{{query}}</a> -->
    </p>
  <% end %>
  

  % if len(docs) == 0:
    <p> No results found. </p>
  <% else:
    for title, link in zip(titles,docs):
  %>
      <div>
      <p class="firstpar" ><a href={{link}}>{{title}}</a></p>
      <p class="nextpar" >{{link}}</p>
      </div>
  %   end
  % end

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
