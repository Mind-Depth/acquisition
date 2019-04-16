package main

import (
	"fmt"
	"net/http"
)

// example of getting post parameter r.FormValue("email")

func handlerToto() {
	http.HandleFunc("/toto", func(writter http.ResponseWriter, req *http.Request) {
		fmt.Fprintf(writter, "I love coconuts")
	})
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Welcome to my website!")
	})

	handlerToto()
	fs := http.FileServer(http.Dir("static/"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}

// package main

// import (
//     "fmt"
//     "log"
//     "net/http"
// )
// func hello(w http.ResponseWriter, r *http.Request) {
//     if r.URL.Path != "/" {
//         http.Error(w, "404 not found.", http.StatusNotFound)
//         return
//     }

//     switch r.Method {
//     case "GET":
//          http.ServeFile(w, r, "form.html")
//     case "POST":
//         // Call ParseForm() to parse the raw query and update r.PostForm and r.Form.
//         if err := r.ParseForm(); err != nil {
//             fmt.Fprintf(w, "ParseForm() err: %v", err)
//             return
//         }
//         fmt.Fprintf(w, "Post from website! r.PostFrom = %v\n", r.PostForm)
//         name := r.FormValue("name")
//         address := r.FormValue("address")
//         fmt.Fprintf(w, "Name = %s\n", name)
//         fmt.Fprintf(w, "Address = %s\n", address)
//     default:
//         fmt.Fprintf(w, "Sorry, only GET and POST methods are supported.")
//     }
// }

// func main() {
//     http.HandleFunc("/", hello)

//     fmt.Printf("Starting server for testing HTTP POST...\n")
//     if err := http.ListenAndServe(":8080", nil); err != nil {
//         log.Fatal(err)
//     }
// }
