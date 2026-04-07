# TMDB CLI Tool
This is a simple tmdb cli that can get the top playing, top rated, upcoming, & most popular movies from [The Movie Database](https://www.themoviedb.org/), project idea [here](https://roadmap.sh/projects/tmdb-cli).

## Setup
 **Clone the Repository**
 ``` bash
    git clone https://github.com/bobthe3rdjrjr/Coding-schtuff.git
    cd ./Coding-schtuff/Tmdb-cli
 ```

 2. **Install Dependencies**
``` bash
pip install -r requirements.txt
```

### Usage
There are 4 different settings:  
* `"playing"`
* `"top"`
* `"upcoming"`
* `"popular"`  

Therefore the usage looks like this:  
``` bash
python tmdb-app --type "playing"  
python tmdb-app --type "popular"
python tmdb-app --type "top"
python tmdb-app --type "upcoming"
```