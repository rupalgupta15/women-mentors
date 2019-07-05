
//const vueApp =

new Vue({               // controls whole or certain part of application - search part
    el: "#vue-app",         // Connects to the DOM
    data: {                 // Different key value pairs in the data object
          name: 'Rupal'
//        return {
//          mentors: [],
//          search:""
//
//        }
    },

    delimiters: ['[[',']]'],

    methods: {

    },

//    computed:{
//    filteredMentors: function(){
//      return this.mentors.filter((mentor) => {
//        return mentor.title.match(this.search);
//            });
//        }
//    },
//    // Only called once at the beginning
//    created(){
//       // we are not sending any data here, so second argument is not needed
//       this.$http.get('https://women-mentoring.firebaseio.com/posts.json').then(function(data){
//           // this.blogs = data.body.slice(0,10); // gets first 10 elements
//           // we are getting array from here and storing in the blogs property above
//           return data.json(); //data.json() is asynchronous task - takes some time to complete
//       }).then(function(data){
//        var mentorsArray = [];
//        for (let key in data){
//          // key refers to the unique id in the database;
//          // data is the parent object which inlcudes the child objects each one being a different blog post
//          data[key].id = key;
//          mentorsArray.push(data[key]);
//        }
//        this.mentors = mentorsArray;
//      });
//    },


});
