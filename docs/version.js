var xhr = new XMLHttpRequest();
xhr.addEventListener('load', function() {
  var version = JSON.parse(this.responseText);
  var footer = document.querySelector('footer');
  var root = document.createElement('div');
  root.setAttribute('id', 'version-info');
  root.innerHTML = '法規版本 '+
  '<a class="commit" href="https://github.com/ntu-student-congress/tortue/commit/'+version.statute+'">'+version.statute.substring(0,7)+'</a>'+
  '，建置版本 '+
  '<a class="commit" href="https://github.com/rschiang/ntusc-statute/commit/'+version.build+'">'+version.build.substring(0,7)+'</a>'+
  ' ('+ version.date +')';
  footer.appendChild(root);
});
xhr.open('GET', (/\/(index\.html)?$/.test(location.href) ? '' : '../') + 'version.json');
xhr.send();
