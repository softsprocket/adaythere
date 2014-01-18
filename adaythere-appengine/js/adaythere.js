
function set_element_positions (width, height) {

	map_width = Math.floor(width * 0.7);
	sidebar_width = Math.floor(width * 0.3); 
	$("#map_section").width (map_width);
	$("#sidebar_section").width (sidebar_width); 
}

function set_section_height (height) {
	h1 = $("#page_header").height();
	h2 = $("#page_footer").height();
	val = height - (h1 + h2);
	$("#map_section").height(val);
	$("#sidebar_section").height(val);
}

/*
 * ADT_GeoLocate location information
 */

function ADT_google_reverse_lookup (latitude, longitude, handler_function) {
	var url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude 
		+ "," + longitude + "&sensor=false";

	return $.get (url, function (response) {
		handler_function (response);
	}, "json");
}

function ADT_GeoLocate () {
	this.location = {

	};

	this.location.latitude = 48.422;
	this.location.longitude = -123.408;
	this.location.locality = "Victoria";
	this.location.address = "Victoria, BC Canada";
}

ADT_GeoLocate.prototype.ipinfo = function () {
	var self = this;
	return $.get("http://ipinfo.io", function (response) {
		var loc = response.loc.split(",");
		self.location.latitude = loc[0];
		self.location.longitude = loc[1];
		self.location.locality = response.city;
		self.location.city = response.city;
		self.location.region = response.region;
		self.location.country = response.country;
	}, "jsonp");
}


ADT_GeoLocate.prototype.geolocate = function () {
	var self = this;
	var deferred = $.Deferred ();
	if (window.navigator.geolocation) {

		window.navigator.geolocation.getCurrentPosition (function (position) {
			self.location.latitude = position.coords.latitude;
			self.location.longitude = position.coords.longitude;
			deferred.resolve ();
		}, function (error) {
			deferred.reject ("Geolocation error: " + error.message);
		}, {timeout:1000});	
	} else {
		deferred.reject ("Geolocation not enabled");
	}

	return deferred;
}

ADT_GeoLocate.prototype.google_reverse_lookup = function (handler_function) {
	ADT_google_reverse_lookup (this.location.latitude, this.location.longitude, handler_function)
}

ADT_GeoLocate.prototype.setRegion = function (data) {
	this.location.locality = data.locality ? data.locality : "";
	this.location.address = data.address ? data.address : "";
}

ADT_GeoLocate.prototype.getLocation = function () {
	return this.location;
}

/*
 * ADT_GoogleMap
 */
function ADT_GoogleMap (latitude, longitude, zoom) {
	zoom = zoom ? zoom : 12;

	var styles = [{
		featureType: "poi",
		elementType: "labels",
		stylers: [
			{ visibility: "off" }
		]
	}];

	var mapOptions = {
		center: new google.maps.LatLng(latitude, longitude),
		zoom: zoom,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		styles: styles
	};

	el = document.getElementById("map_section");
	this.map = new google.maps.Map(el, mapOptions);
	this.map.setOptions({styles: styles});
	this.placesService = new google.maps.places.PlacesService(this.map);
}

ADT_GoogleMap.prototype.get = function () {
	return this.map;
}


/*
 * ADT_GoogleReverseLookup
 */

function ADT_getLocality (address_components) {
	var result = null;

	for (var addr_index in address_components) {
		var address =  address_components[addr_index];
		if ((address.types.indexOf("locality") != -1) && (address.types.indexOf("political") != -1)) {
			result = address.long_name;
		} 
	} 

	return result;
}

function ADT_GoogleReverseLookup (data) {
	this.data = data.results;
	this.status = (data.status == "OK" ? true : false);
}

ADT_GoogleReverseLookup.prototype.location = function () {
	var result = {};

	if (this.status) {
		 result.locality = ADT_getLocality (this.data[0].address_components);
		 result.address = this.data[0].formatted_address;
	}

	return { status: this.status, result: result };
}

/*
 * adaythere angular module
 */
var adaythere = angular.module("adaythere", []);

/*
 * Create location service
 */
function ADT_LocationInitializerService () {
	this.geoloc = new ADT_GeoLocate ();
	this.geocoder = new google.maps.Geocoder();
	this.map = null;
	this.autocomplete = null;
}

ADT_LocationInitializerService.prototype.getLocation = function () {
	return this.geoloc.getLocation ();
}

ADT_LocationInitializerService.prototype.initialize = function () {
	var deferred = $.Deferred ();
	self = this;
	this.geoloc.geolocate ().fail (function (err_msg) {
		console.error (err_msg);
	}).always (function () {
		self.map = new ADT_GoogleMap (self.geoloc.location.latitude, self.geoloc.location.longitude);

		self.geoloc.google_reverse_lookup (function (response) {
			var lookup = new ADT_GoogleReverseLookup (response);
			var res = lookup.location ();
			if (res.status) {
				self.geoloc.setRegion (res.result);
			}

			var input = document.getElementById ("pac_input");
			var div = document.getElementById ("search_util");

			self.autocomplete = new google.maps.places.Autocomplete(input);
			self.autocomplete.bindTo("bounds", self.map.get ());
			deferred.resolve (self.geoloc);
		});
	});

	return deferred;
}

ADT_LocationInitializerService.prototype.placeChange = function (scope, place) {

	if (!place.geometry) {
		return;
	}

	if (place.geometry.viewport) {
		this.map.get ().fitBounds(place.geometry.viewport);
	} else {
		this.map.get ().setCenter(place.geometry.location);
	}

	var locality = ADT_getLocality (place.address_components);
	var address = place.formatted_address;

	self.geoloc.setRegion ({locality: locality, address: address});

	scope.$apply(function () {
		scope.location = self.geoloc.location;
	});
}

adaythere.factory ("locationInitializer", function () {
	return new ADT_LocationInitializerService ();
});

/*
 * adaythere controllers
 */

adaythere.controller ("sidebarCtrl", ["$scope", "locationInitializer", function ($scope, locationInitializer) {
	$scope.location = locationInitializer.getLocation ();
	$scope.clicked = {
		latitude: "",
		longitude: "",
		locality: "",
		address: ""
	}


	$scope.types = [ "airport", "amusement_park", "aquarium", "art_gallery", "bakery", "bar", 
		"beauty_salon", "bicycle_store", "book_store", "bowling_alley", "cafe", "casino", 
		"cemetery", "church", "city_hall", "clothing_store", "department_store", "establishment",
		"florist", "food", "gym", "hair_care", "hindu_temple", "jewelry_store", "library",
		"liquor_store", "meal_takeaway", "mosque", "movie_theater", "museum", "night_club",
		"park", "place_of_worship", "restaurant", "shoe_store", "shopping_mall", "spa", "stadium",
		"store", "synagogue", "university", "zoo"
	];

	$scope.type = "all";

	var lastClicked;

	locationInitializer.initialize ().then (function (geoloc) {
		$scope.$apply(function () {
			$scope.location = geoloc.location;
		});

		var moved = false;

		google.maps.event.addListener (locationInitializer.map.get (), "center_changed", function() {
			var latlng = locationInitializer.map.get ().getCenter();
			locationInitializer.geoloc.location.latitude = latlng.lat ();
			locationInitializer.geoloc.location.longitude = latlng.lng ();

			moved = true;

			$scope.$apply(function () {
				$scope.location = locationInitializer.geoloc.location;
			});

		});


		var timerId;
		google.maps.event.addListener (locationInitializer.map.get (), "click", function(event) {
			timerId = window.setTimeout (function () {
			
				ADT_google_reverse_lookup (event.latLng.lat (), event.latLng.lng (), function (response) {
					var rlu = new ADT_GoogleReverseLookup (response);
					var clicked = rlu.location ().result;

					clicked.latitude = event.latLng.lat ();
					clicked.longitude = event.latLng.lng ();
					lastClicked = event.latLng;

					$scope.$apply(function () {
						$scope.clicked = clicked;
					});
				});

			}, 250);

		});

		google.maps.event.addListener (locationInitializer.map.get (), "dblclick", function(event) {
			window.clearTimeout (timerId);
		});

		google.maps.event.addListener (locationInitializer.map.get (), "mouseup", function() {
			if (moved) {
				moved = false;
				locationInitializer.geoloc.google_reverse_lookup (function (response) { 
					var lookup = new ADT_GoogleReverseLookup (response);
					var res = lookup.location ();

					if (res.status) {
						locationInitializer.geoloc.setRegion (res.result);
					}

					$scope.$apply(function () {
						$scope.location = locationInitializer.geoloc.location;
					});


				});
			}
		});

		google.maps.event.addListener (locationInitializer.autocomplete, "place_changed", function() {
			
			var place = locationInitializer.autocomplete.getPlace();
			locationInitializer.placeChange ($scope, place);
		});
	});

	$scope.go = function () {
		var address = $("#pac_input").val ();
		locationInitializer.geocoder.geocode( { "address": address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var place = results[0];
				locationInitializer.placeChange ($scope, place);
			} else {
				console.error ("Geocode was not successful for the following reason: " + status);
			}
		});

	};

	$scope.search_places = function () {
		if (!lastClicked) {
			console.log ("No click yet");
			return;
		}

		console.log ($scope.type);
		service = locationInitializer.map.placesService;

		var sel_types = [];
		if (!$scope.type || $scope.type == "all") {
			sel_types = $scope.types;
		} else {
			sel_types.push ($scope.type);
		}	

		var request = {
			location: lastClicked,
			radius: "500",
			types: sel_types
		};

		service.nearbySearch(request, function (results, status) {
			if (status == google.maps.places.PlacesServiceStatus.OK) {
				for (var i = 0; i < results.length; i++) {
					var place = results[i];
					console.log (JSON.stringify (place));
				}
			}
		});

	};
}]);

adaythere.controller ("menuCtrl", ["$scope", "$http", function ($scope, $http) {
	$scope.userLogout = function( user) {
		$http.get ( "/usermenu?logout=" + user)
			.success (function(data, status, headers, config) {
				//this.query_data = data;
				//$scope.places = data;
			}
		);

	};

	$scope.userLogin = function (user) {
		$http.get ("/usermenu?login=" + user)
			.success (function(data, status, headers, config) {
				//this.query_data = data;
				//$scope.places = data;
			}
		);
	};			
}]);

adaythere.controller( "twitterQueryCtrl", ["$scope", "$http", function($scope, $http) {
	this.query_data = null;
	$scope.setPlace = function (place) {
		$http.get ("/places?place=" + place)
			.success (function(data, status, headers, config) {
				this.query_data = data;
				$scope.places = data;
			});

	};
}]);

/*
 * jquery callbacks
 */
$(window).resize (function () {
	var width = $(window).width();
	var height = $(window).height();

//	set_element_positions (width, height);

	set_section_height (height);

})


$(function () {

	var width = $(window).width();
	var height = $(window).height();
	
	set_section_height (height);
//	set_element_positions (width, height);
	console.log (width + " " + height);

})



