function    createApp() {
     const allcomps = new jpComponentBuilder.App({
     target: document.getElementById("components"),
     props: {
       name: "world",
       atag: "span",
       justpyComponents : justpyComponents
     },
     });
  
  
  return allcomps;
  

}
