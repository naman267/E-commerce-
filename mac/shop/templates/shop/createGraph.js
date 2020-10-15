


export function track(city)
{
dict={};
function creategraph(V,E)
{
  let adjlist=[];
  for(let i=0;i<V;i++)
  {
    adjlist.push([]);
  }
  for(let i=0;i<E.length;i++)
  {
  	adjlist[dict[E[i][0]]].push( [dict[E[i][1]],E[i][2]] );

    adjlist[dict[E[i][1]]].push( [ dict[E[i][0]] , E[i][2] ] );
  }
  return adjlist;
}

function djikstra(graph, V, src) {
    let vis = Array(V).fill(0);
    let dist = [];
    for(let i=0;i<V;i++)
        dist.push([10000,-1]);
    dist[src][0] = 0;

    for(let i=0;i<V-1;i++){
        let mn = -1;
        for(let j=0;j<V;j++){
            if(vis[j]===0){
                if(mn===-1 || dist[j][0]<dist[mn][0])
                    mn = j;
            }
        }

        vis[mn] = 1;
        for(let j=0;j<graph[mn].length;j++){
            let edge = graph[mn][j];
            if(vis[edge[0]]===0 && dist[edge[0]][0]>dist[mn][0]+edge[1]){
                dist[edge[0]][0] = dist[mn][0]+edge[1];
                dist[edge[0]][1] = mn;
            }
        }
    }

    return dist;
}

let cities=['Delhi', 'Mumbai', 'Gujarat', 'Goa'];
let V=cities.length;

for(let i=0;i<V;i++)
{
	dict[cities[i]]=i
}
console.log(dict);
let E=[];
for(let i=0;i<V;i++)
{
	for(let j=i+1;j<V;j++)
	{
		let weight=Math.floor(Math.random() * 70) + 30;
		E.push([cities[i],cities[j],weight]);
	}
}
console.log(E);
graph=creategraph(V,E);
console.log(graph);
let distances = djikstra(graph,V,2);
console.log(distances);
dest=dict[city];


let path=[];

let parent=distances[dest][1];

while(dest!=-1)
{
	path.push(dest);
	dest=distances[dest][1];
}
console.log(path);

creat();

function create()
{

    // create a network
    const container = document.getElementById('graph');
    const genNew = document.getElementById('generate-graph');

    // initialise graph options

    const options = {
        edges: {
            labelHighlightBold: true,
            font: {
                size: 20
            }
        },
        nodes: {
            font: '12px arial-red',
            scaling: {
                label: true
            },
            shape: 'icon',
            icon: {
                face: 'FontAwesome',
                code: '\uf015',
                size: 40,
                color: '#991133'
            }
        }
    };

    // initialize your network!
    const network = new vis.Network(container);
    network.setOptions(options);

    function createdata()
    {

        // Initialising number of nodes in graph dynamically
        //const V = Math.floor(Math.random() * cities.length) + 3;
    const V=cities.length;
        // Preparing node data for Vis.js
        let vertices = [];
        for (let i = 0; i < path.length; i++) {
            vertices.push({ id: i, label: cities[path[i]] });
        }

        // Preparing edges for Vis.js
        let edges = [];
        for (let i = 0; i < path.length; i++) {
            // Picking a neighbour from 0 to i-1 to make edge to
            for(let j=i+1;j<V;j++)
            {
            let neigh = j;//Math.floor(Math.random() * i);

            // Adding the edge between node and neighbour
            edges.push({ from: i, to: neigh, color: 'orange', label: String(graph[i]) });
            }
        }

        //Preparing data object for Vis.js
        const data = {
            nodes: vertices,
            edges: edges
        };
        return data;
    
 }
    genNew.onclick = function() {
        // Creating and setting data to network
        let data = createdata();
        network.setData(data);
    };

    genNew.click();

};
};