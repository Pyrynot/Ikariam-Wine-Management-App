const BACKEND_URL = "http://localhost:8000";

// Reusable fetch operation
async function makeFetchRequest(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Failed to fetch: ${response.statusText}`);
  }
  return response.json();
}

export function fetchTowns() {
  return makeFetchRequest(`${BACKEND_URL}/towns/`);
}

export function transferWine(playerName, sourceTown, destinationTown, wineAmount) {
    // Parsing the wine amount to float
    const parsedWineAmount = parseFloat(wineAmount);
  
    return makeFetchRequest(`${BACKEND_URL}/towns/transfer/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        player_name: playerName,
        source_town_name: sourceTown,
        destination_town_name: destinationTown,
        wine_amount: parsedWineAmount,
      }),
    });
  }

export function addTown(playerName, townName, wineStorage, wineHourlyConsumption, wineProduction) {
    // Make sure these field names match the schema expected by your backend
    const townData = {
      player_name: playerName,  // field names should match the backend model exactly
      town_name: townName,
      wine_storage: parseFloat(wineStorage),  // ensure this is a float, not a string
      wine_hourly_consumption: parseFloat(wineHourlyConsumption),  // ensure this is a float, not a string
      wine_production: parseFloat(wineProduction),  // ensure this is a float, not a string
    };
  
    console.log('Sending town data:', townData);
  
    return makeFetchRequest(`${BACKEND_URL}/towns/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(townData),
    });
  }
  

export function updateTown(townId, data) {
  return makeFetchRequest(`${BACKEND_URL}/towns/${townId}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
}

export function deleteTown(townId) {
  return makeFetchRequest(`${BACKEND_URL}/towns/${townId}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
    // No body is needed for a DELETE request
  });
}