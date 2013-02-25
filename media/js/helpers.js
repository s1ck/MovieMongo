function format_result(result){
  img_url = result.img_url ? result.img_url : "http://img.freebase.com/api/trans/image_thumb/freebase/no_image_png";
  url = result._id.$oid;//source+"?id="+result.id;
  
  if (result.my_movie === true)
    status = "<a href='#' id='del_movie' title='" + $.i18n("Remove movie from collection") + "' onclick=\"return del_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check del'></i>"
    + "</a>";
  else
    status = "<a href='#' id='add_movie' title='" + $.i18n("Add movie to collection") + "' onclick=\"return add_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check add'></i>"
    + "</a>";
  
  return "<li class='media thumbnail'>"
    + "<div class='media-body'>"
    + "  <a class='pull-left' href='/"+url+"'>"
    + "    <img class='media-object result' src='" + img_url + "' /> "
    + "  </a>"
    + "  <a href='/"+url+"'><h3 id='name' class='media-heading'>"+result.name+"</h3></a>&nbsp;"
    + status
    + "  <p>" + $.i18n("Source") + ": " + result.source + "</p>"
    + "</div>"
    + "</li>";
}

function format_details(result){
  img_url = result.img_url ? result.img_url : "http://img.freebase.com/api/trans/image_thumb/freebase/no_image_png";
  if (result.my_movie)
    status = "<a href='#' id='del_movie' title='" + $.i18n("Remove movie from collection") + "' onclick=\"return del_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check del'></i>"
    + "</a>";
  else
    status = "<a href='#' id='add_movie' title='" + $.i18n("Add movie to collection") + "' onclick=\"return add_movie(event,\'"+result._id.$oid+"\');\">"
    +   "<i class='icon-check add'></i>"
    + "</a>";
  
  out = "<div class='media-body thumbnail' style='padding:10px'>"
    + "  <img class='media-object result pull-left' style='margin-right:10px' src='" + img_url + "' /> "
    + "  <h3 id='name' class='media-heading'>"+result.name+"</h3> "
    + status
    + "<p><strong>"+ $.i18n("Source") + ":</strong> " + result.source;
  
  if (result.links && result.links.length > 0){
    out += "<br/><strong>" + $.i18n("other sources") + ": </strong>";
    for (link in result.links)
      out += "<a href='" + result.links[link].oid.$oid + "'>" + result.links[link].target + "</a> ";
  }
  out += "</p>";
  out += "  <hr/><div class='pull-left'><h4>Details:</h4><dl class='dl-horizontal'>";
  out += result.actors.length > 0 ? "<dt>"+ $.i18n("actors") + ":</dt><dd><ul><li>" + result.actors.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.directed_by.length > 0 ? "<dt>" + $.i18n("directed_by") + ":</dt><dd><ul><li>" + result.directed_by.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.genre.length > 0 ? "<dt>" + $.i18n("genre") + ":</dt><dd><ul><li>" + result.genre.join("</li><li>") + "</li></ul></dd>" : "";
  out += result.initial_release_date ? "  <dt>" + $.i18n("released") + ":</dt><dd>" + result.initial_release_date + "</dd>" : "";
  out += result.written_by.length > 0 ? "<dt>" + $.i18n("written by") + ":</dt><dd><ul><li>" + result.written_by.join("</li><li>") + "</li></ul></dd>" : "";
  out += "</dl></div>";
  if (result.my_movie){
    out += "<span id='usercontent'></span>"
    get_usercontent(result._id.$oid);
  }
  out += "</div>";
  return out;
}

function add_movie(event, id){
  console.log(event);
  event.preventDefault();
  $.ajax({
    url: "http://localhost:8080/",
    type: "POST",
    data: {id: id},
    success: function(data){
      $("#add_movie").remove();
      $("#name").after(" <a href='#' id='del_movie' title='Remove movie from collection' onclick=\"return del_movie(event,\'"+id+"\')\">"
				   +   "<i class='icon-check del'></i>"
				   + "</a>");
      
      console.log("success");
    }
  });
  //return false;
}

function del_movie(event, id){
  console.log(event);
  event.preventDefault();
  $.ajax({
    url: "http://localhost:8080/",
    type: "DELETE",
    data: {id: id},
    success: function(data){
      $("#del_movie").remove();
      $("#name").after(" <a href='#' id='add_movie' title='Add movie to collection' onclick=\"return add_movie(event,\'"+id+"\')\">"
				   +   "<i class='icon-check add'></i>"
				   + "</a>");

      console.log("success");
    }
  });
  //return false;
}
