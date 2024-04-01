import React, { useState, useMemo } from 'react';
import './TownStyles.css';
import TownUpdateForm from './TownUpdateForm';
import TownDeleteButton from './TownDeleteButton';

function calculateTimeRemaining(town) {
  const netConsumption = town.wine_production - town.wine_hourly_consumption;
  if (netConsumption >= 0) {
    return '∞';
  }
  
  // Calculate total hours remaining
  let hoursRemaining = town.wine_storage / Math.abs(netConsumption);
  
  // Convert hours to months, days, hours, and minutes
  const months = Math.floor(hoursRemaining / (24 * 30));
  hoursRemaining -= months * 24 * 30;
  const days = Math.floor(hoursRemaining / 24);
  hoursRemaining -= days * 24;
  const hours = Math.floor(hoursRemaining);
  const minutes = Math.floor((hoursRemaining - hours) * 60);

  // Format the string
  let result = '';
  if (months > 0) result += `${months}M `;
  if (days > 0 || months > 0) result += `${days}D `;
  result += `${hours}h ${minutes}m`;

  return result;
}

function getStyleForTimeRemaining(timeRemaining) {
  if (timeRemaining === '∞') {
    return {}; // No special styling for infinite time
  }
  
  // Extract numbers from the formatted string
  const matches = timeRemaining.match(/(\d+)M|(\d+)D|(\d+)h|(\d+)m/g);
  let totalHours = 0;

  matches.forEach(match => {
    const value = parseInt(match);
    if (match.includes('M')) {
      totalHours += value * 24 * 30; // Convert months to hours
    } else if (match.includes('D')) {
      totalHours += value * 24; // Convert days to hours
    } else if (match.includes('h')) {
      totalHours += value;
    } else if (match.includes('m')) {
      totalHours += value / 60; // Convert minutes to hours
    }
  });

  // Determine styling based on total hours remaining
  if (totalHours < 72) { // Less than 3 days
    return { backgroundColor: 'red' };
  } else if (totalHours < 168) { // Less than 7 days
    return { backgroundColor: 'orange' };
  }

  return {}; // Default, no special styling
}

function DisplayTowns({ towns, onUpdateSuccess, fetchAndUpdateTowns }) {
  const [editingTownId, setEditingTownId] = useState(null);

  const townsByPlayer = useMemo(() => {
    const groups = {};
    towns.forEach(town => {
      const playerName = town.player_name;
      const updateTime = new Date(town.last_update);
      if (!groups[playerName]) {
        groups[playerName] = { towns: [], lastUpdate: updateTime };
      }
      groups[playerName].towns.push(town);
      if (groups[playerName].lastUpdate < updateTime) {
        groups[playerName].lastUpdate = updateTime;
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
                <th>Time remaining</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {playerData.towns.map((town) => {
                const timeRemaining = calculateTimeRemaining(town);
                const rowStyle = getStyleForTimeRemaining(timeRemaining);
                return (
                  <tr key={town.id} style={rowStyle}>
                    <td>{town.town_name}</td>
                    <td>{town.wine_storage.toFixed(2)}</td>
                    <td>{town.wine_hourly_consumption.toFixed(2)}</td>
                    <td>{town.wine_production.toFixed(2)}</td>
                    <td>{timeRemaining}</td>
                    <td>
                      {editingTownId === town.id ? (
                        <TownUpdateForm
                          town={town}
                          onUpdateSuccess={() => {
                            setEditingTownId(null);
                            fetchAndUpdateTowns();
                          }}
                          onCancel={() => setEditingTownId(null)}
                          fetchAndUpdateTowns={fetchAndUpdateTowns}
                        />
                      ) : (
                        <>
                          <button onClick={() => setEditingTownId(town.id)}>Edit</button>
                          <TownDeleteButton
                            townId={town.id}
                            onDeleteSuccess={fetchAndUpdateTowns}
                            fetchAndUpdateTowns={fetchAndUpdateTowns}
                          />
                        </>
                      )}
                    </td>
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
