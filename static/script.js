const BASE_URL = "http://LOCALHOST:5000";

async function getCupcakes() {
  // GET request to API to grab all cupcakes

  const response = await axios.get(`${BASE_URL}/api/cupcakes`);

  cupcakeFlavors = response.data.cupcakes;
  // console.log(cupcakeFlavors);
  for (let i=0; i<cupcakeFlavors.length; i++) {
    let cupcake = generateCupcakeHTML(cupcakeFlavors[i]);
    $('.cupcakes').append(cupcake);
  }

  return response;
}

function generateCupcakeHTML(cupcake) {
  // Generate individual cupcake list elements

  const cupcakeMarkup = $(`
    <li id="${cupcake.id}">
      <div>${cupcake.flavor}</div>
      <div>${cupcake.size}</div>
      <div>${cupcake.rating}</div>
      <img class= 'images' src=${cupcake.image}></img>
    </li>
  `);
  return cupcakeMarkup;
}

$('.add-cupcake').on('submit', addCupcakeHandler);

async function addCupcakeHandler(evt) {
  // Event handler for adding new cupcake FORMS

  evt.preventDefault();

  let flavor = $('.flavor').val();
  let size = $('.size').val();
  let rating = $('.rating').val();
  let image = $('.image').val();

  console.log(flavor);
  
  const response = await axios.post(`${BASE_URL}/api/cupcakes`, 
      {'flavor': flavor, 'size': size, 'rating': rating, 'image': image,}
  )

  let cupcake = generateCupcakeHTML(response.data.cupcake);
  $('.cupcakes').append(cupcake);

}

// Run getCupcakes onload
$(getCupcakes);