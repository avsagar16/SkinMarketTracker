import React, { useState } from 'react';
import { Search, Loader2, AlertCircle, TrendingUp, Package } from 'lucide-react';

const CounterStrikeSkinTracker = () => {
  const [steamId, setSteamId] = useState('');
  const [skins, setSkins] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async () => {
    if (!steamId.trim()) {
      setError('Please enter a Steam ID');
      return;
    }

    setLoading(true);
    setError('');
    setHasSearched(true);

    try {
      // Replace with your actual backend URL
      const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: steamId.trim(),
            timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch skins');
      }

      const data = await response.json();
      setSkins(data);
    } catch (err) {
      setError('Failed to load skins. Please check the Steam ID and try again.');
      setSkins([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const formatPrice = (price) => {
    if (typeof price === 'number') {
      return `$${price.toFixed(2)}`;
    }
    return price || 'N/A';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Animated background effect */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2 tracking-tight">
            Counter Strike Skin Tracker
          </h1>
          <p className="text-gray-400">Track and monitor your CS2 inventory value</p>
        </div>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="relative group">
            <input
              type="text"
              value={steamId}
              onChange={(e) => setSteamId(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter your Steam ID..."
              className="w-full px-6 py-4 pr-14 bg-gray-800 border-2 border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-orange-500 transition-all duration-300 text-lg"
            />
            <button
              onClick={handleSearch}
              disabled={loading}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-3 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-600 rounded-lg transition-all duration-300 group-hover:scale-105"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 text-white animate-spin" />
              ) : (
                <Search className="w-5 h-5 text-white" />
              )}
            </button>
          </div>
          
          {error && (
            <div className="mt-4 p-4 bg-red-900/30 border border-red-500 rounded-lg flex items-center gap-2 text-red-400">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="w-12 h-12 text-orange-500 animate-spin mb-4" />
            <p className="text-gray-400 text-lg">Loading your inventory...</p>
          </div>
        )}

        {/* Skins Grid */}
        {!loading && hasSearched && skins.length > 0 && (
          <div className="max-w-7xl mx-auto">
            <div className="mb-6 p-4 bg-gray-800/50 rounded-lg backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Package className="w-5 h-5 text-orange-500" />
                  <span className="text-white font-semibold">Total Items: {skins.length}</span>
                </div>
                {skins.some(skin => skin.price) && (
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-500" />
                    <span className="text-white font-semibold">
                      Total Value: {formatPrice(skins.reduce((sum, skin) => sum + (skin.price || 0), 0))}
                    </span>
                  </div>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {skins.map((skin, index) => (
                <div
                  key={index}
                  className="bg-gray-800/50 backdrop-blur-sm rounded-xl overflow-hidden border border-gray-700 hover:border-orange-500 transition-all duration-300 hover:transform hover:scale-105 hover:shadow-2xl group"
                >
                  {/* Skin Image */}
                  <div className="aspect-video bg-gradient-to-br from-gray-700 to-gray-800 relative overflow-hidden">
                    {skin.image ? (
                      <img
                        src={skin.image}
                        alt={skin.name}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <Package className="w-12 h-12 text-gray-600" />
                      </div>
                    )}
                    
                    {/* Wear Badge */}
                    {skin.wear && (
                      <div className="absolute top-2 right-2 px-2 py-1 bg-black/70 rounded text-xs text-white backdrop-blur-sm">
                        {skin.wear}
                      </div>
                    )}

                    {/* Price Overlay */}
                    {skin.price && (
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3">
                        <p className="text-green-400 font-bold text-lg">{formatPrice(skin.price)}</p>
                      </div>
                    )}
                  </div>

                  {/* Skin Details */}
                  <div className="p-4">
                    <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2 group-hover:text-orange-400 transition-colors">
                      {skin.name || 'Unknown Skin'}
                    </h3>
                    
                    {skin.type && (
                      <p className="text-gray-500 text-xs mb-2">{skin.type}</p>
                    )}

                    {/* Additional Info */}
                    <div className="flex items-center justify-between mt-3">
                      {skin.rarity && (
                        <span className={`text-xs px-2 py-1 rounded ${
                          skin.rarity.toLowerCase() === 'covert' ? 'bg-red-900/50 text-red-400' :
                          skin.rarity.toLowerCase() === 'classified' ? 'bg-pink-900/50 text-pink-400' :
                          skin.rarity.toLowerCase() === 'restricted' ? 'bg-purple-900/50 text-purple-400' :
                          skin.rarity.toLowerCase() === 'mil-spec' ? 'bg-blue-900/50 text-blue-400' :
                          'bg-gray-700 text-gray-400'
                        }`}>
                          {skin.rarity}
                        </span>
                      )}
                      
                      {skin.statTrak && (
                        <span className="text-xs px-2 py-1 rounded bg-orange-900/50 text-orange-400">
                          StatTrak™
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && hasSearched && skins.length === 0 && !error && (
          <div className="text-center py-20">
            <Package className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 text-lg">No marketable skins found for this Steam ID</p>
          </div>
        )}

        {/* Initial State */}
        {!loading && !hasSearched && (
          <div className="text-center py-20">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gray-800 rounded-full mb-4">
              <Search className="w-10 h-10 text-gray-600" />
            </div>
            <p className="text-gray-400 text-lg">Enter a Steam ID to view CS2 inventory</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CounterStrikeSkinTracker;