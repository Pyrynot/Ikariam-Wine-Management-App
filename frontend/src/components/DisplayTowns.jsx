import React, { useMemo } from 'react';
import './TownStyles.css';

function calculateTimeRemaining(town) {
    const netConsumption = town.wine_production - town.wine_hourly_consumption;
    // If production is greater than or equal to consumption, return infinity
    if (netConsumption >= 0) {
      return '∞';
    }
    const timeRemaining = town.wine_storage / Math.abs(netConsumption);
    return timeRemaining.toFixed(2); // Keep only two decimal places
  }

function getStyleForTimeRemaining(timeRemaining) {
    if (timeRemaining === '∞') {
      return {}; // No special styling for infinite time
    }
    const hoursRemaining = parseFloat(timeRemaining);
    if (hoursRemaining < 72) {
      return { backgroundColor: 'red' }; // Less than 72 hours
    } else if (hoursRemaining < 168) {
      return { backgroundColor: 'orange' }; // Less than 168 hours
      
    }
    return {}; // Default, no special styling
  }

  function DisplayTowns({ towns }) {
    const townsByPlayer = useMemo(() => {
      const groups = {};
      towns.forEach(town => {
        if (!groups[town.player_name]) {
          groups[town.player_name] = {
            towns: [],
            lastUpdate: new Date(town.last_update)
          };
        }
        groups[town.player_name].towns.push(town);
        if (groups[town.player_name].lastUpdate < new Date(town.last_update)) {
          groups[town.player_name].lastUpdate = new Date(town.last_update);
        }
      });
      return groups;
    }, [towns]);
  
    return (
      <div className="table-container">
        {Object.entries(townsByPlayer).map(([playerName, playerData]) => (
          <div key={playerName} className="player-section">
            <h3>{playerName}'s Towns, last updated: {playerData.lastUpdate.toLocaleString()}</h3>
            <table>
              <thead>
                <tr>
                  <th>Town Name</th>
                  <th>Wine Storage</th>
                  <th>Wine Hourly Consumption</th>
                  <th>Wine Production</th>
                  <th>Time remaining (hours)</th>
                </tr>
              </thead>
              <tbody>
                {playerData.towns.map((town) => {
                  const timeRemaining = calculateTimeRemaining(town);
                  const style = getStyleForTimeRemaining(timeRemaining);
                  return (
                    <tr key={town.id}>
                      <td>{town.town_name}</td>
                      <td>{town.wine_storage.toFixed(2)}</td>
                      <td>{town.wine_hourly_consumption.toFixed(2)}</td>
                      <td>{town.wine_production.toFixed(2)}</td>
                      <td style={style}>{timeRemaining}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    );
  }
  

export default DisplayTowns;
