var ADT_Constants = {
	MINIMUM_WINDOW_WIDTH:  900,
	DEFAULT_MAP_ZOOM: 12
};

function ADT_set_section_height (height) {
	var h1 = $("#page_header").height ();
	var h2 = $("#page_footer").height ();
	var val = height - (h1 + h2);
	$("#map_section").height (val);
	$("#sidebar_section").height (val);
	$("#welcome_to_left").height (val);
	$("#welcome_to_right").height (val);
	$("#find_a_day").height (val);	
}

function ADT_shallow_copy (obj) {
	var copy;

	if (Object.prototype.toString.call (obj) === '[object Array]') {
		copy = [];
	} else {
		copy = {};
	}

	for (var index in obj) {
		if (obj.hasOwnProperty (index)) {
	       		copy[index] = obj[index];
	 	}
	}

	return copy;	
}

function ADT_swap_with_next (arr, index) {
	var removed = arr.splice (index, 1);
	arr.splice (parseInt (index) + 1, 0, removed[0]);
}

function ADT_swap_with_prev (arr, index) {
	var removed = arr.splice (index, 1);
	arr.splice (parseInt (index) - 1, 0, removed[0]);
}

function ADT_string_trim (str) {
	return str.replace (/^\s+|\s+$/gm,'');
}

function ADT_Apply (scope, func) {
	if (scope) {
		var phase = scope.$root.$$phase;
		if (phase == '$apply' || phase == '$digest') {
			func ();
		} else {
			var self = this;
			scope.$apply (func);
		}
	}
}

function ADT_DirectionsRenderer (map) {
	this.directionsService = new google.maps.DirectionsService ();
	this.directionsDisplay = new google.maps.DirectionsRenderer ();
	this.directionsDisplay.setOptions ( { suppressMarkers: true } );

	this.map = map;
}

ADT_DirectionsRenderer.prototype.showDirections = function (day, mode) {

	if (day.places.length <= 1) return;

	var to_index = day.places.length - 1;

	var from = day.places[0];
	var to = day.places[to_index];

	var start = new google.maps.LatLng (
		from.location.latitude, 
		from.location.longitude
	);

	var end = new google.maps.LatLng (
		to.location.latitude, 
		to.location.longitude
	);


	var waypoints = [];

	if (to_index > 1) {
		for (var ind = 1; ind < to_index; ++ind) {
			waypoints.push ({ 
				location: new google.maps.LatLng (
					day.places[ind].location.latitude,
					day.places[ind].location.longitude
				)
			});
		}
	}

	var request = {
		origin:start,
		destination:end,
		waypoints: waypoints,
		travelMode: mode
	};

	var self = this;	
	
	this.directionsDisplay.setMap (this.map);
	this.directionsService.route (request, function (result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			self.directionsDisplay.setDirections (result);
		} else {
			console.log (status);
			console.log (result);
		}
	});
}

ADT_DirectionsRenderer.prototype.hideDirections = function () {
	this.directionsDisplay.setMap (null);
};

/*
 * ADT_CreatedDay
 */

function ADT_Place () {
	this.name = "";
	this.comment = "";
	this.location = {};
	this.vicinity = "";
	this.types = [];

	this.marker = null;
}

ADT_Place.prototype.equals = function (place) {
	return (place.name == this.name) && (place.vicinity == this.vicinity);
}

ADT_Place.from_marker_content = function (marker_content) {
	var place = new ADT_Place ();
	for (var index in marker_content) {
		if (marker_content.hasOwnProperty (index)) {
			if (index == "location") {
				place.location.latitude = marker_content.location.latitude;
				place.location.longitude = marker_content.location.longitude;
			} else if (index == "name") {
				place.name = marker_content.name;
			} else if (index == "comment") {
				place.comment = marker_content.comment;
			} else if (index == "vicinity") {
				place.vicinity = marker_content.vicinity;
			} else if (index == "is_editable") {
				place.is_editable = marker_content.is_editable;
			} else if (index == "types") {
				place.types = marker_content.types;
			}
		}
	}

	return place;
}

function ADT_DayPhoto () {
	this.title = ""
	this.description = ""
}

function ADT_CreatedDay () {
	this.title = "";
	this.keywords = "";
	this.description = "";
	this.places = [];
	this.photos = [];
	this.full_locality = "";

	this.markers_visible = false;
}

ADT_CreatedDay.prototype.is_cleared = function () {

	return ((this.title == "")  &&  (this.keywords == "")
		&& (this.description == "") && (this.places.length == 0) 
		&& (this.photos.length == 0) && (this.full_locality == ""));
};

ADT_CreatedDay.prototype.clear = function () {
	this.title = "";
	this.description = "";
	this.keywords = "";
	this.full_locality = ""
	for (var index in this.places) {
		if (this.places[index].marker) {
			this.places[index].marker.setMap (null);
		}
	}

	this.places = [];
	this.photos = [];
};

ADT_CreatedDay.prototype.top_places_list = function (place) {
	return this.places[0].equals (place);
};

ADT_CreatedDay.prototype.bottom_places_list = function (place) {
	return this.places[this.places.length - 1].equals (place);
};

ADT_CreatedDay.prototype.swap_with_next = function (index) {
	var removed = this.places.splice (index, 1);
	this.places.splice (parseInt (index) + 1, 0, removed[0]);
};

ADT_CreatedDay.prototype.swap_with_prev = function (index) {
	var removed = this.places.splice (index, 1);
	this.places.splice (parseInt (index) - 1, 0, removed[0]);
};

ADT_CreatedDay.prototype.remove = function (place) {
	var tmp_places = [];

	for (var index in this.places) {
		var saved_place = this.places[index];
		if (place.equals (saved_place)) {
			place.marker.setMap (null);
		} else {
			tmp_places.push (saved_place);
		}
	}

	this.places = tmp_places;
};

ADT_CreatedDay.prototype.moveup = function (place) {
	for (var index in this.places) {
		var saved_place = this.places[index];
		if (place.equals (saved_place)) {
			if (index != 0) {
				this.swap_with_prev (index);
				break;
			} else {
				return;
			}
		}
	}
};

ADT_CreatedDay.prototype.movedown = function (place) {
	var last_index = this.places.length - 1;
	for (var index in this.places) {
		var saved_place = this.places[index];
		if (place.equals (saved_place)) {
			if (index != last_index) { 
				this.swap_with_next (index);
				break;
			} else {
				return;
			}
		}
	}
};

ADT_CreatedDay.prototype.to_json = function () {
	var day = new ADT_CreatedDay ();
	day.title = this.title;
	day.keywords = this.keywords;
	day.description = this.description;
	day.full_locality = this.full_locality;

	for (var index = 0; index < this.places.length; ++index) {
		var place = new ADT_Place ();
        	place.name = this.places[index].name;
	        place.comment = this.places[index].comment;
		place.location.latitude = this.places[index].location.latitude;
		place.location.longitude = this.places[index].location.longitude;
		place.vicinity = this.places[index].vicinity;

		day.places.push (place);
	}

	for (var index = 0; index < this.photos.length; ++index) {
		var photo = new ADT_DayPhoto ();
		photo.description = this.photos[index].description;
		photo.title = this.photos[index].title;
		day.photos.push (photo);	
	}


	return JSON.stringify (day);	
};

ADT_CreatedDay.copy = function (created_day) {
	var day = new ADT_CreatedDay ();

	day.title = created_day.title;
	day.keywords = created_day.keywords;
	day.description = created_day.description;
	day.full_locality = created_day.full_locality;

	day.is_editable = created_day.is_editable;
	day.is_collapsed = created_day.is_collapsed;

	for (var index in created_day.places) {
		var place = new ADT_Place ();
		place.name = created_day.places[index].name;
		place.comment = created_day.places[index].comment;
		place.location.latitude = created_day.places[index].location.latitude;
		place.location.longitude = created_day.places[index].location.longitude;

		place.vicinity =  created_day.places[index].location.vicinity ? created_day.places[index].location.vicinity : created_day.places[index].vicinity;

		day.places.push (place);
	}

	for (var index = 0; index < created_day.photos.length; ++index) {
		var photo = new ADT_DayPhoto ();
		photo.description = created_day.photos[index].description;
		photo.title = created_day.photos[index].title;
		day.photos.push (photo);	
	}

	return day;
}

var execute_mail_function;

ADT_CreatedDay.prototype.show_markers = function (scope, map) {
	var markerBounds = new google.maps.LatLngBounds ();

	var add_listener = function (marker, place) {
	
		var timer = null;
		google.maps.event.addListener (marker, "click", function () {
			if (timer) {
				clearTimeout (timer);
				timer = null;

			}
			scope.adt_marker_modal.open_marker_modal (place, false, false);
		});

		var infowindow = new google.maps.InfoWindow ({
			content: "<a href='javascript:execute_mail_function ()'>You could advertise here - click for more information</a>"
		});

		google.maps.event.addListener (place.marker, 'mouseover', function () {
			timer = setTimeout (function () {
				infowindow.open (map, place.marker);
			}, 1000);
		});

		google.maps.event.addListener (place.marker, 'mouseout', function () {
			if (timer) {
				clearTimeout (timer);
				timer = null;
			}
		});
	};
	
	for (var each in this.places) {
		var markerPosition = new google.maps.LatLng (this.places[each].location.latitude, this.places[each].location.longitude);
		this.places[each].marker = new google.maps.Marker ({
			position: markerPosition,
			map: map
		});

		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
		this.places[each].marker.setIcon (iconFile);

		add_listener (this.places[each].marker, this.places[each]);

		markerBounds.extend (markerPosition);

	}

	map.fitBounds (markerBounds);

	this.markers_visible = true;
}

ADT_CreatedDay.prototype.hide_markers = function () {
	for (var index = 0; index < this.places.length; ++index) {
		if (this.places[index].marker) {
			this.places[index].marker.setMap (null);
		}
	}

	this.markers_visible = false;
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

function ADT_GeoLocate (location_promise) {
	this.location = {};
	this.location_promise = location_promise;
	this.default_location_set = false;
}

ADT_GeoLocate.prototype.setDefault = function () {

	var self = this;

	return this.location_promise.then (function (data) {
		if (data && !isNaN (data.latitude)) {
			self.location.latitude = data.latitude;
			self.location.longitude = data.longitude;
			self.location.locality = data.locality;
			self.location.vicinity = data.vicinity ? data.vicinity : data.address;
			self.location.full_locality = data.full_locality ? data.full_locality : self.location.vicinity;
			self.default_location_set = true;
		} else {

			self.location.latitude = 48.422;
			self.location.longitude = -123.408;
			self.location.locality = "Victoria";
			self.location.vicinity = "Victoria,BC,Canada";
			self.location.full_locality = self.location.vicinity;
		}
	}, function () {

		self.location.latitude = 48.422;
		self.location.longitude = -123.408;
		self.location.locality = "Victoria";
		self.location.vicinity = "Victoria,BC,Canada";
		self.location.full_locality = self.location.vicinity;
	});
}

ADT_GeoLocate.prototype.geolocate = function () {
	var self = this;
	var deferred = $.Deferred ();

	this.setDefault ().then (function () {
		
		if (self.default_location_set == true) {
			deferred.resolve ();
		} else {
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
		}

	});

	return deferred;
}

ADT_GeoLocate.prototype.google_reverse_lookup = function (handler_function) {
	ADT_google_reverse_lookup (this.location.latitude, this.location.longitude, handler_function)
}

ADT_GeoLocate.prototype.setRegion = function (data) {
	this.location.locality = data.locality ? data.locality : null;
	this.location.region = data.region ? data.region : null;
	this.location.country_name = data.country_name ? data.country_name : null;
	this.location.full_locality = (this.location.locality != null ? this.location.locality + "," : "")
		+ (this.location.region != null ? this.location.region + "," : "")
		+ (this.location.country_name != null ? this.location.country_name : "");


	this.location.vicinity = (data.vicinity != null ? data.vicinity: this.location.full_locality);

	console.log ("ADT_Geolocate setRegion", this.location.full_locality);
}

ADT_GeoLocate.prototype.getLocation = function () {
	return this.location;
}

/*
 * ADT_GoogleMapService
 */
function ADT_GoogleMapService (loc) {

	this.geoloc = new ADT_GeoLocate (loc);
	this.geocoder = new google.maps.Geocoder ();
	this.map = null;
	this.autocomplete = null;
	this.boundsCircle = null;
	this.search_area_is_visible = false;
	this.timerId = null;
	
	this.clicked = {
		latitude: "",
		longitude: "",
		locality: "",
		vicinity: ""
	}

	this.location = this.geoloc.location;
	this.moved = false;
	this.placesService = null;
	this.directionsRenderer = null;
}


ADT_GoogleMapService.prototype.initialize = function (scope) {
	var deferred = $.Deferred ();
	self = this;
	
	this.geoloc.geolocate ().fail (function (err_msg) {
		console.error ("GoogleMapService initialize: geolocate", err_msg);
	}).always (function () {

		var styles = [{
			featureType: "poi",
			elementType: "labels",
			stylers: [
				{ visibility: "off" }
			]		
		}];

		var mapOptions = {
			center: new google.maps.LatLng (self.geoloc.location.latitude, self.geoloc.location.longitude),
			zoom: ADT_Constants.DEFAULT_MAP_ZOOM,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			styles: styles
		};

		var el = document.getElementById ("map_section");
		self.map = new google.maps.Map (el, mapOptions);
		self.map.setOptions ({styles: styles});
		self.placesService = new google.maps.places.PlacesService (self.map);

		var input = document.getElementById ("autocomplete_google_input");
		var div = document.getElementById ("location_search_util");

		self.autocomplete = new google.maps.places.Autocomplete (input);
		self.autocomplete.bindTo ("bounds", self.map);

		self.boundsCircle = new ADT_BoundingCircle (self.map);

		google.maps.event.addListener (self.map, 'bounds_changed', function () {
			self.boundsCircle.updateBounds (self.map.getBounds ());
			self.boundsCircle.updateStatus (self.search_area_is_visible);
		});


		google.maps.event.addListener (self.map, "click", function (event) {
		       	self.set_search_location (event, scope);
		});
		
		self.boundsCircle.addClickListener (function (event) {
			self.set_search_location (event, scope);
		});

		google.maps.event.addListener (self.map, "dblclick", function (event) {
			window.clearTimeout (self.timerId);
		});
		
		google.maps.event.addListener (self.map, "center_changed", function () {
			var latlng = self.map.getCenter ();
			self.location.latitude = latlng.lat ();
			self.location.longitude = latlng.lng ();

			self.moved = true;

			self.clicked = self.location;

		});

		google.maps.event.addListener (self.map, "mouseup", function () {
			if (self.moved) {
				self.moved = false;
				self.geoloc.google_reverse_lookup (function (response) { 
					var lookup = new ADT_GoogleReverseLookup (response);
					var res = lookup.location ();

					if (res.status) {
						self.geoloc.setRegion (res.result);
					}

				});
			}
		});

		google.maps.event.addListener (self.autocomplete, "place_changed", function () {
			var place = self.autocomplete.getPlace ();
			self.placeChange (place);
			$("#centre_map_at_button").trigger ("click");
		});


		self.directionsRenderer = new ADT_DirectionsRenderer (self.map);

		if (self.geoloc.location.vicinity) {
			deferred.resolve (self.geoloc);
		} else {
			self.geoloc.google_reverse_lookup (function (response) {
				var lookup = new ADT_GoogleReverseLookup (response);
				var res = lookup.location ();
				if (res.status) {
					self.geoloc.setRegion (res.result);
				}

				deferred.resolve (self.geoloc);
			});
		}

	});

	return deferred;
}

ADT_GoogleMapService.prototype.get = function () {
	return this.map;
}

ADT_GoogleMapService.parse_region = function (spans) {
	var loc = {};

	var regex = new RegExp ("<\s*span[^<]*>[^<>]*<\/\s*span\s*>", "gi");
	var matches = spans.match (regex);

	$.each (matches, function (i, el) {
		var adr = $.parseHTML (el);

		if ($(adr)[0].className) {
			if ($(adr)[0].className == 'locality') {
				loc.locality = $(adr)[0].innerText;
			} else if ($(adr)[0].className == 'region') {
				loc.region = $(adr)[0].innerText;
			} else if ($(adr)[0].className == 'country-name') {
				loc.country_name = $(adr)[0].innerText;
			}
		}
	});

	return loc;
}

ADT_GoogleMapService.prototype.placeChange = function (place) {
	
	if (place.adr_address) {
		console.log ("ADT_GoogleMapService.placeChange", place.adr_address);
		var loc = ADT_GoogleMapService.parse_region (place.adr_address);		
		self.geoloc.setRegion (loc);
	}

	if (!place.geometry) {
		return;
	}

	if (place.geometry.viewport) {
		this.map.fitBounds (place.geometry.viewport);
	} else {
		this.map.setCenter (place.geometry.location);
	}


}


ADT_GoogleMapService.prototype.set_search_location = function (event, scope) {
	var self = this;
	this.timerId = window.setTimeout (function () {

		self.map.setCenter (event.latLng);

		self.boundsCircle.setCenter (event.latLng);
		self.boundsCircle.updateStatus (self.search_area_is_visible);

		ADT_google_reverse_lookup (event.latLng.lat (), event.latLng.lng (), function (response) {
			var rlu = new ADT_GoogleReverseLookup (response);
			var clicked = rlu.location ().result;

			clicked.latitude = event.latLng.lat ();
			clicked.longitude = event.latLng.lng ();

			scope.$apply (function () {
				self.clicked = clicked;
			});

		});

	}, 250);
};


/*
 * ADT_GoogleReverseLookup
 */

function ADT_getFullLocality (address_components) {
	var result = {};

	for (var addr_index in address_components) {
		var address =  address_components[addr_index];
		if ((address.types.indexOf ("locality") != -1) && (address.types.indexOf ("political") != -1)) {
			result.locality = address.long_name;
		} else if ((address.types.indexOf ("administrative_area_level_1") != -1) && (address.types.indexOf ("political") != -1)) {
			result.region = address.short_name;
		} else if ((address.types.indexOf ("country") != -1) && (address.types.indexOf ("political") != -1)) {
			result.country_name = address.long_name;
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
		 result = ADT_getFullLocality (this.data[0].address_components);
		 result.address = this.data[0].formatted_address;
	}

	return { status: this.status, result: result };
}


/*
 * adaythere angular module
 */
var adaythere = angular.module ("adaythere", ['ui.bootstrap', 'ngRoute']);

adaythere.factory ("googleMapService", [ "profileService", function (profileService) {
	return new ADT_GoogleMapService (profileService.getLocation ());
}]);

/*
 * Search service
 */

function ADT_SearchService ($http, $q) {
	this.$http = $http;
	this.$q = $q;
	this.locality_autocomplete = null;
	this.locality_input = null;
	this.full_locality = "";

}

ADT_SearchService.prototype.init = function () {
	this.locality_input = document.getElementById ('locality_autocomplete_input');
	this.locality_autocomplete = new google.maps.places.Autocomplete (this.locality_input);

	if (this.locality_autocomplete == null) {
		console.error ("Autocomplete", "unable to create");
	} else {
		this.locality_autocomplete.setTypes (['geocode']);
		
		var self = this;	
		google.maps.event.addListener(this.locality_autocomplete, 'place_changed', function () {
			var place = self.locality_autocomplete.getPlace ();
			if (!place.geometry) {
				console.error ("Not a place", place);
				return;
			}

			console.log ("ADT_SearchService", place);
			var data = ADT_GoogleMapService.parse_region (place.adr_address);

			var locality = data.locality ? data.locality : null;
			var region = data.region ? data.region : null;
			var country_name = data.country_name ? data.country_name : null;
			var full_locality = (locality != null ? locality + "," : "")
				+ (region != null ? region + "," : "")
				+ (country_name != null ? country_name : "");

			self.full_locality = full_locality;
			console.log ("ADT_SearchService", self.full_locality);
		});
	}
}

adaythere.factory ("searchService", ["$http", "$q", function ($http, $q) {
	return new ADT_SearchService ($http, $q);
}]);

/*
 * Create Profile service
 */
function ADT_ProfileService ($http, $q) {
	this.$http = $http;
	this.$q = $q;
}

ADT_ProfileService.prototype.getLocation = function () {
	var deferred = this.$q.defer ();

	this.getUserProfile ().then (function (data) {
		if (data.location) {
			deferred.resolve (data.location);
		} else {
			deferred.resolve (null);
		}
	}, function (data, status) {
		console.error (status, data);
	});

	return deferred.promise;	
}

ADT_ProfileService.prototype.getUserProfile = function () {
	var deferred = this.$q.defer ();
	var self = this;

	if (this.profile_data) {
		deferred.resolve (this.profile_data)
		this.update = false;
	} else {
		this.$http ({
			method: "GET",
			url: "/profile"
		}).success (function (data, status, headers, config) {
			self.profile_data = data; 
			self.updated = true;    
			deferred.resolve (data); 
		}).error (function (data, status, headers, config) {
			deferred.reject (data, status);
		});
	}

	return deferred.promise;
}

ADT_ProfileService.prototype.setUserLocation = function (location) {
	var self = this;

	this.$http ({
		method: "POST",
		url: "/profile",
		data: { location: location }
	}).success (function (data, status, headers, config) {
		self.profile_data = data;
	}).error (function (data, status, headers, config) {
		console.error (status, data);
	});

}

ADT_ProfileService.prototype.add_tool_access = function (name) {
	var deferred = this.$q.defer ();
	var self = this;

	this.$http ({
		method: "PUT",
		url: "/profile?operation=add_tool_access&name=" + name
	}).success (function (data, status, headers, config) {
		deferred.resolve (data)
	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.resolve (data);
	});

	return deferred.promise;
}

adaythere.factory ("profileService", ["$http", "$q", function ($http, $q) {
	return new ADT_ProfileService ($http, $q);
}]);

/*
 * ADT_UserDaysService
 */
function ADT_UserDaysService ($http, $q) {
	this.$http = $http;
	this.$q = $q;
	
	this.user_days = [];
	this.deleted_days = [];
}

ADT_UserDaysService.prototype.getDays = function () {
	var deferred = this.$q.defer ();
	var self = this;

	if (this.user_days.length > 0) {
		deferred.resolve (this.user_days);
	} else {
		this.$http.get ("/days").success (function (data, status, headers, config) {
			for (var each in data) {
				var day = JSON.parse (data[each]);
				day.is_editable = false;
				day.is_collapsed = true;

				self.user_days.push (ADT_CreatedDay.copy (day));
			}

			deferred.resolve (this.user_days);

		}).error (function (data, status, headers, config) {
			console.error (status, data);
			deferred.reject ();
		});
	}

	return deferred.promise;
};

ADT_UserDaysService.prototype.addDay = function (created_day) {
	var day = ADT_CreatedDay.copy (created_day);
	
	var self = this;
	this.$http.put ("/days", day.to_json ()).success (function (data, status, headers, config) {
		day.is_collapsed = false;
		for (var index in self.user_days) {
			self.user_days[index].is_collapsed = true;
		}

		day.is_editable = false;
		
		self.user_days.push (day);

	}).error (function (data, status, headers, config) {
		console.error (status, data);
	});
}

ADT_UserDaysService.prototype.updateDay = function (updated_day) {
	var day = ADT_CreatedDay.copy (updated_day);

	var self = this;
	this.$http.post ("/days", day.to_json ()).success (function (data, status, headers, config) {
	
	}).error (function (data, status, headers, config) {
		console.error (status, data);
	});

};

ADT_UserDaysService.prototype.deleteDay = function (deleted_day) {
	var deferred = this.$q.defer ();
	var day = ADT_CreatedDay.copy (deleted_day);
	var self = this;
	this.$http.delete ("/days", { params: { title: day.title }}).success (function (data, status, headers, config) {

		for (i in self.user_days) {

			if (self.user_days[i] == deleted_day) {
				self.user_days.splice (i, 1);
				self.deleted_days.push (deleted_day);
				break;
			}
		}

		deferred.resolve ();	
	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.reject ();
	});
	
	return deferred.promise;
};

ADT_UserDaysService.prototype.removeDeletedDay = function (deleted_day) {
	for (i in this.deleted_days) {
		if (this.deleted_days[i] == deleted_day) {
			this.deleted_days.splice (i, 1);
		}
	}

};

adaythere.factory ("userDaysService", ["$http", "$q", function ($http, $q) {
	return new ADT_UserDaysService ($http, $q);
}]);

/*
 *  
 *  ADT_LocalityDaysService
 *  
 */

function ADT_LocalityDaysService ($http, $q) {
	this.$http = $http;
	this.$q = $q;
	this.keywords = []
}

ADT_LocalityDaysService.prototype.getDays = function (params) {
	var deferred = this.$q.defer ();
	var self = this;

	var config = {
		params : params
	};

	this.$http.get ("/locality_days", config).success (function (data, status, headers, config) {
		deferred.resolve (data);
	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.reject ();
	});


	return deferred.promise;
};

ADT_LocalityDaysService.prototype.getKeywords = function () {
	var deferred = this.$q.defer ();
	var self = this;

	this.$http.get ("/keywords").success (function (data, status, headers, config) {
		self.keywords = [];
		for (var i = 0; i < data.length; ++i) { 
			self.keywords.push (data[i])
		}

		deferred.resolve (data)

	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.reject ();
	});

	return deferred.promise;
};

adaythere.factory ("localityDaysService", ["$http", "$q", function ($http, $q) {
	return new ADT_LocalityDaysService ($http, $q);
}]);


function ADT_PhotoService ($http, $q) {
	this.$http = $http;
	this.$q = $q;
	
	this.total_allowed_photos = 50;
	this.current_count = 0;
	this.title_list = []

	this.getTitles ();
}

ADT_PhotoService.prototype.getCurrentCount = function () {

	var deferred = this.$q.defer ();
	var self = this;

	if (this.current_count > 0) {
		deferred.resolve (this.current_count);
	} else {
		this.$http.get ("/photos?action=count").success (function (data, status, headers, config) {
			current_count = data.coount;
			deferred.resolve (data.count);

		}).error (function (data, status, headers, config) {
			console.error (status, data);
			deferred.reject ();
		});
	}

	return deferred.promise;
};

ADT_PhotoService.prototype.upload = function (photos) {

	var deferred = this.$q.defer ();
	var self = this;

	this.$http.put ("/photos", JSON.stringify (photos)).success (function (data, status, headers, config) {

		self.current_count += photos.length;

		var len = photos.length;
		
		for (var i = 0; i < len; ++i) {
			self.title_list.push (photos[i]);
		}

		deferred.resolve ();
	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.reject ();
	});


        return deferred.promise;

}

ADT_PhotoService.prototype.getTitles = function () {
	var deferred = this.$q.defer ();
	var self = this;

	if (this.title_list.length > 0) {
		deferred.resolve (this.title_list);
	} else {
		this.$http.get ("/photos?action=list").success (function (data, status, headers, config) {
		
			for (var i = 0; i < data.length; ++i) {
				self.title_list.push (data[i]);
			}
			self.current_count = self.title_list.length;

			deferred.resolve ();
		}).error (function (data, status, headers, config) {
			console.error (status, data);
			deferred.reject ();
		});
	}

	return deferred.promise;
}

ADT_PhotoService.prototype.deleteTitles = function (titles, used_by) {
	var deferred = this.$q.defer ();
	var qstr = "/photos?titles=";
	var sep = "";
	for (var i= 0; i < titles.length; ++i) {
		qstr += sep;
		qstr += titles[i];
		sep = ",";
	}

	if (used_by) {
		qstr += "&used_by=";
		qstr += used_by
	}

	self = this;

	this.$http.delete (qstr).success (function () {
		deferred.resolve ();
	}).error (function (data, status, headers, config) {
		console.error (status, data);
		deferred.reject ();
	});

	return deferred.promise;
}

adaythere.factory ("photoService", ["$http", "$q", function ($http, $q) {
	return new ADT_PhotoService ($http, $q);
}]);

/*
 * adaythere controllers
 */

function ADT_BoundingCircle (map) {
	this.map = map;
	this.boundsCircle = null;
	this.circleOptions = {
		strokeColor: '#FF0000',
		strokeOpacity: 0.8,
		strokeWeight: 2,
		fillColor: '#FF0000',
		fillOpacity: 0.35,
		map: this.map,
		clickable: true
	};
}

ADT_BoundingCircle.prototype.updateBounds = function (bounds) {
	var sw = bounds.getSouthWest ();
	var ctr = bounds.getCenter ();
	var lat;
	var lng;

	if (sw.lat () > sw.lng ()) {
		lat = sw.lat ();
		lng = ctr.lng ();
	} else {
		lat = ctr.lat ();
		lng = sw.lng ();
	}

	var left = new google.maps.LatLng (lat, lng);
	var diff = google.maps.geometry.spherical.computeDistanceBetween (left, ctr);

	if (diff > 50000) {
		diff = 50000;
	}

	this.circleOptions.center = ctr;
	this.circleOptions.radius = diff;
}

ADT_BoundingCircle.prototype.setCircle = function () {

	if (this.boundsCircle) {
		this.boundsCircle.setMap (null);
	}

	this.boundsCircle = new google.maps.Circle (this.circleOptions);
	if (this.clickListener) {
		google.maps.event.addListener (this.boundsCircle, "click", this.clickListener);
	}
}

ADT_BoundingCircle.prototype.unsetCircle = function () {
	if (this.boundsCircle) {
		this.boundsCircle.setMap (null);
	}
}

ADT_BoundingCircle.prototype.setCenter = function (center) {
	this.circleOptions.center = center;
}

ADT_BoundingCircle.prototype.getCenter = function () {
	return this.circleOptons.center;
}

ADT_BoundingCircle.prototype.setRadius = function (radius) {
	this.circleOptions.radius = radius;
}

ADT_BoundingCircle.prototype.getRadius = function () {
	return this.circleOptions.radius ? this.circleOptions.radius : 0;
}

ADT_BoundingCircle.prototype.updateStatus = function (visible) {
	if (visible) {
		this.setCircle ();
	} else {
		this.unsetCircle ();
	}
}

ADT_BoundingCircle.prototype.addClickListener = function (listener) {
	this.clickListener = listener;
}

function ADT_DaysSearchMap (element_id, location) {
	var styles = [{
		featureType: "poi",
		elementType: "labels",
		stylers: [
			{ visibility: "off" }
		]
	}];

	var mapOptions = {
		center: new google.maps.LatLng (location.latitude, location.longitude),
		zoom: ADT_Constants.DEFAULT_MAP_ZOOM,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		styles: styles
	};

	var el = document.getElementById (element_id);
	this.map = new google.maps.Map (el, mapOptions);
	this.map.setOptions ({styles: styles});

}

function ADT_UserRatingService (http, q) {
	this.http = http;
	this.q =q;
}

ADT_UserRatingService.prototype.send_rating = function (userid, title, rating, text) {
	var qstr = '/user_comments';
        var deferred = this.q.defer ();
	
	var data = {
		userid: userid,
		title: title,
		rating:rating,
		text: text
	};

	this.http.put (qstr, data).success (function (data, status, headers, config) {
		var o = {
			data: data,
			status: status
		};
		deferred.resolve (o);
	}).error (function (data, status, headers, config) {
		var o = {
			data: data,
			status: status
		};
		deferred.reject (o);	        
	});
	
	return deferred.promise;
}

ADT_UserRatingService.prototype.get_ratings = function (userid, title, index, limit, cursor) {
	var qstr = '/user_comments?';
        var deferred = this.q.defer ();
	
	var join = '&';
	qstr += 'userid=';
	qstr += userid;
	qstr += join;
	qstr += 'title=';
	qstr += title;

	if (limit || cursor) {
		if (limit) {
			qstr += join;
			qstr += 'limit=';
			qstr += limit;
		}
	
		if (cursor) {
			qstr += join;
			qstr += 'cursor='
			qstr += cursor;
		}
	}

	this.http.get (qstr).success (function (data, status, headers, config) {
		var o = {
			index: index,
			more: data.more,
			cursor: data.cursor,
			comments: [],
			status: status
		};

		for (var i = 0; i < data.comments.length; ++i) {
			o.comments.push (JSON.parse (data.comments[i]));
		}

		deferred.resolve (o);
	}).error (function (data, status, headers, config) {
		var o = {
			data: data,
			status: status
		};
		deferred.reject (o);	        
	});
	
	return deferred.promise;
}

adaythere.factory ("userRatingService", ["$http", "$q", function ($http, $q) {
	return new ADT_UserRatingService ($http, $q);
}]);

adaythere.controller ("daysSearchCtrl", ["$scope", "$modal", "localityDaysService", "profileService", 
		"searchService", "googleMapService", "userRatingService", "$timeout", "$location",
		function ($scope, $modal, localityDaysService, profileService, searchService, googleMapService, userRatingService, $timeout, $location) {

	searchService.init ();

	$scope.adt_marker_modal = new ADT_MarkerModal ($scope, googleMapService.get (), $modal);

	$scope.daysearch = {};
	$scope.daysearch.selected_keywords = [];
	$scope.daysearch.keywords = localityDaysService.keywords;
	$scope.daysearch.full_locality = searchService.full_locality;
	$scope.daysearch.words = "";
	$scope.daysearch.all_words = "any";
	$scope.daysearch.rating = 0;
	$scope.daysearch.max = 10;

	$scope.$watch(function(localityDaysService) { return localityDaysService.keywords },
              function() { $scope.daysearch.keywords = localityDaysService.keywords; }
        );

	var init_return = function () {
		$scope.daysearch_returned = {};
		$scope.daysearch_returned.days = [];
		$scope.daysearch_returned.msg_to_user = "";
		$scope.user_comments = [];
		$scope.daysearch_returned.reviews = [];
	}

	var hello_world = function () {
		if ($("#user_not_logged_in").length == 0) {
			return;
		}
	
		$("#hello_login_popup").show (2000, function () {
			$("#hello_search_popup").show (2000, function () {
				$("#hello_help_popup").show (2000);	
			});	
		});	
	}


	init_return ();

	hello_world ();

	$scope.open_welcome_doors = function () {
		$("#welcome_to_left").hide ("slow");
		$("#welcome_to_right").hide ("slow");
		$("#daysearch_overlay").slideUp ();
	};

	$scope.return_to_daysearch = function () {
		$("#welcome_to_left").show ("fast");
		$("#welcome_to_right").show ("fast");
		$("#daysearch_overlay").slideDown ();
	};

	localityDaysService.getKeywords ().then (function () {
		$scope.daysearch.keywords = localityDaysService.keywords;
	});


	$scope.getRandomDays = function () {
		$("#hello_login_popup").hide ();
		$("#hello_search_popup").hide ();
		$("#hello_help_popup").hide ();
		$scope.getLocalityDays ({random:true});
		$scope.open_welcome_doors ();
	};

	function UserComment () {
		this.collapsed = true;
		this.rated = false;
		this.rating = 0;
		this.text = "";
		this.max = 10;
	};

	$scope.user_comments = [];
	
	$scope.getLocalityDays = function (params) {
		init_return ();
		localityDaysService.getDays (params).then (function (data) {
			if (!data || data.days.length == 0) {
				$scope.daysearch_returned.msg_to_user = "Search returned empty";
			} else {
				$scope.daysearch_returned.msg_to_user = "Search results";
				for (var i = 0; i < data.days.length; ++i) { 
					var day = JSON.parse (data.days[i]);
					day.is_collapsed = true;
					day.is_editable = false;
					$scope.daysearch_returned.days.push (day);

					userRatingService.get_ratings (day.userid, day.title, i).then (function (o) {
						if (o.status == 200 || o.status == 201) {
							$scope.daysearch_returned.reviews[o.index] = o.comments;
							if (o.status == 201) {
								$scope.user_comments[o.index] = new UserComment ();
								$scope.user_comments[o.index].rated = true;
							}
						} else {

							$scope.daysearch_returned.reviews[o.index] = null; 
						}
					});
				}
			}
		});	
	};

	$scope.day_toggle_open = function (day) {
		day.is_collapsed = !day.is_collapsed;
	}

	$scope.executeSearch = function () {
		$("#hello_login_popup").hide ();
		$("#hello_search_popup").hide ();
		$("#hello_help_popup").hide ();

		$scope.daysearch.full_locality = searchService.full_locality;

		if ($scope.daysearch.full_locality == "") {
			$("#locality_autocomplete_input").click (function () {
				$("#locality_autocomplete_input").css ("border", "").val ("");
			});

			$("#locality_autocomplete_input").css ("border", "1px solid red").val ("required field")

			return;
		}
		
		$scope.open_welcome_doors ();

		var keywords = "";
		var len = $scope.daysearch.selected_keywords.length;
		for (var i = 0; i < len; ++i) {
			var sep = (i + 1) == len ? "" : ","
			keywords = keywords + $scope.daysearch.selected_keywords[i]  + sep;
		}

		args = {}
		if (keywords != "") {
			args.keywords = keywords;
		}

		if ($scope.daysearch.words != "") {
			args.words = $scope.daysearch.words;
		}

		if ($scope.daysearch.locality != "") {
			args.full_locality = $scope.daysearch.full_locality
		}

		args.minimum_rating = $scope.daysearch.rating;
			
		args.all_words =  ($scope.daysearch.all_words == "all");

		$scope.getLocalityDays (args);
	};



	$scope.open_dayview_rater = function (index) {

		if (!$scope.user_comments[index]) {
			$scope.user_comments[index] = new UserComment ();
		}

		$scope.user_comments[index].collapsed = false;
	};

	$scope.save_user_comment = function (day, index) {
		$scope.user_comments[index].collapsed = true;

		userRatingService.send_rating (day.userid, day.title, $scope.user_comments[index].rating, $scope.user_comments[index].text)
		.then (function (o) {
			$scope.daysearch_returned.days[index].numberOfReviews = o.data.numberOfReviews;
			$scope.daysearch_returned.days[index].averageReview = o.data.averageReview;
			$scope.user_comments[index].rated = true;
			console.log (index, $scope.daysearch_returned);
			$scope.daysearch_returned.reviews[index].push (o.data.review);
		}, function (o) {
			if (o.status == 401) {
				console.error ("Permission denied");					
			} else if (o.status == 409) {
				console.error ("previous rating", o.data);
			} else {
				console.error (o.status, o.data);
			}
		});

		$scope.user_comments[index].text= "";
		$scope.user_comments[index].rating = 0;
	};

	$scope.cancel_user_comment = function (index) {
		$scope.user_comments[index].collapsed = true;
		$scope.user_comments[index].text= "";
		$scope.user_comments[index].rating = 0;
	};

	$scope.search_displayed_maps = [];
	$scope.search_displayed_direction_renderer = [];
	$scope.direction_modes = [
		"Driving",
                "Walking",
		"Bicycling"
	];

	$scope.direction_mode = [];

	$scope.show_map_of = function (day, index) {
		var show_map = $("#dayssearch_show_map_button"+index).html () == "View Map";
		var sel = 'googlemap_of_'+index;

		if (show_map) {
			$("#daysearch_travelmode_selector"+index).show ();
			var width = $("#daysearch_return_display").width ();
			$("#"+sel).css ({
				"height": "400px"
			});
			
			if (!$scope.search_displayed_maps[index]) {
				$scope.direction_mode[index] = "Driving";
				$scope.search_displayed_maps[index] = new ADT_DaysSearchMap (sel, day.places[0].location);

				var created_day = ADT_CreatedDay.copy (day);
				created_day.show_markers ($scope, $scope.search_displayed_maps[index].map);

				$("#daysearch_travelmode_selector"+index).change (function () { 
					console.log ("selector");
					switch ($scope.direction_mode[index]) {
						case "Driving":
							mode = google.maps.TravelMode.DRIVING;
				       			break;
						case "Walking":
							mode = google.maps.TravelMode.WALKING;
							break;
						case "Bicycling":
							mode = google.maps.TravelMode.BICYCLING;
							break;
						default:
							mode = google.maps.TravelMode.DRIVING;
							break;	
					};		
					$scope.search_displayed_direction_renderer[index].showDirections (day, mode);
				});

				$scope.search_displayed_direction_renderer[index] = new ADT_DirectionsRenderer ($scope.search_displayed_maps[index].map);
				$scope.search_displayed_direction_renderer[index].showDirections (created_day, google.maps.TravelMode.DRIVING);
			}
			$("#dayssearch_show_map_button"+index).html ("Hide Map");
		} else {
			$("#daysearch_travelmode_selector"+index).hide ();
			$("#dayssearch_show_map_button"+index).html ("View Map");
			$("#"+sel).css ({ "height":0 });
		}
	};

	$scope.show_review_display = [];
	$scope.show_reviews_for = function (index) {
		$scope.show_review_display[index] = !$scope.show_review_display[index];
	};

	$scope.open_google_plus_window = function (userid, title) {
		var url = "https://plus.google.com/share?url=" + encodeURIComponent ("//www.adaythere.com/?userid=" + userid + "&title=" + title);
		window.open(url, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
	};


	var url = document.URL;
	var parser = document.createElement('a');
	parser.href = url;
	if (parser.search != "") {
		var decoded_search = decodeURI (parser.search);
		var values = decoded_search.split (/[?&]/);
		var args = {};
		for (var i = 0; i < values.length; ++i) {
			if (values[i] == "") continue;

			var kv = values[i].split ("=");
			args[kv[0]] = kv[1];
		}
		
		$timeout (function () {
			$scope.getLocalityDays (args);
			$scope.open_welcome_doors ();
		});
	}
	
}]);

adaythere.run (function ($rootScope) {
	$rootScope.execute_report_function;
});

adaythere.controller ("loginCtrl", ["$rootScope", "$scope", "$http", "$modal", function ($rootScope, $scope, $http, $modal) {

	$scope.googlelogin = function () {
		$http.get ("/login?method=google")
			.success (function (data, status, headers, config) {
				window.location.href = data.url;
			}
		);
	};
	
	$scope.googlelogout = function () {
		$http.get ("/logout?method=google")
			.success (function (data, status, headers, config) {
				window.location.href = data.url;
			}
		);
	};

	$scope.open_help = function () {
		var modalInstance = $modal.open ({
			templateUrl: 'helpModalContent.html',
		    	controller: adaythere.HelpModalInstanceCtrl,
		    	scope: $scope,
		});
	};

	$scope.open_contact = function () {
		var modalInstance = $modal.open ({
			templateUrl: 'mailModalContent.html',
		    	controller: adaythere.SendMailModalInstanceCtrl,
		    	scope: $scope,
		});

		modalInstance.result.then (function (data) {
			$http.post ("/send", JSON.stringify (data))
				.success (function (data, status) {
					console.log ("message sent: " + status);	
				})
	       			.error (function (data, status) {
					console.error ("message send failed: " + data);
				});	
		}, function () {
			
		});
	};


	execute_mail_function = $scope.open_contact;
	
	$scope.open_report = function (type, obj) {
		console.log (type, obj);

		var modalInstance = $modal.open ({
			templateUrl: 'reportModalContent.html',
		    	controller: adaythere.ReportModalInstanceCtrl,
		    	scope: $scope,
		    	resolve: {
		    		type: function () { return type; },
		    		obj: function () { return obj; }
			}
		});

		modalInstance.result.then (function (data) {
			$http.post ("/send", JSON.stringify (data))
				.success (function (data, status) {
					console.log ("message sent: " + status);	
				})
	       			.error (function (data, status) {
					console.error ("message send failed: " + data);
				});	
		}, function () {
			
		});
	};

	$rootScope.execute_report_function = $scope.open_report;
}]);

adaythere.SendMailModalInstanceCtrl = function ($scope, $modalInstance, $http) {


	$scope.send = function () {
		var data = {};
		var ok = true;

		if ($("#mail_form_email").length != 0) {
			data.sender = $("#mail_form_email").val ();
			if (data.sender == "") {
				ok = false;

				$("#mail_form_email").click (function () {
					$("#mail_form_email").css ("border", "").val ("");
				});

				$("#mail_form_email").css ("border", "1px solid red").val ("required field")
			}
		}

		data.subject = $("#mail_form_subject").val ();
		if (data.subject == "") {
			ok = false;

			$("#mail_form_subject").click (function () {
				$("#mail_form_subject").css ("border", "").val ("");
			});

			$("#mail_form_subject").css ("border", "1px solid red").val ("required field")
		}

		data.body = $("#mail_form_message").val ();
		if (data.body == "") {
			ok = false;

			$("#mail_form_message").click (function () {
				$("#mail_form_message").css ("border", "").val ("");
			});

			$("#mail_form_message").css ("border", "1px solid red").val ("required field")
		}
		
		data.name = $("#mail_form_name").val ();
		
		if (ok) {
			$modalInstance.close (data);
		}
	};

	$scope.cancel = function () {
		$modalInstance.dismiss ('cancel');
	};

};

adaythere.ReportModalInstanceCtrl = function ($scope, $modalInstance, $http, type, obj) {

	console.log ("In instance:", type, obj);

	$scope.report_subject = "Reported: " + type + " Name: " + (obj.name ? obj.name : obj.commenters_name) + " Title: " + obj.title;

	$scope.send = function () {
		var data = {};
		var ok = true;

		data.subject = $("#report_form_subject").val ();

		data.body = $("#report_form_message").val ();
		if (data.body == "") {
			ok = false;

			$("#report_form_message").click (function () {
				$("#report_form_message").css ("border", "").val ("");
			});

			$("#report_form_message").css ("border", "1px solid red").val ("required field")
		}
		
		data.name = $("#report_form_name").val ();
		
		if (ok) {
			data.body += "\n----------------------------------------\n";
			data.body += (obj.description ? obj.description : obj.text);
			console.log (data.body);
			$modalInstance.close (data);
		}
	};

	$scope.cancel = function () {
		$modalInstance.dismiss ('cancel');
	};

};

adaythere.HelpModalInstanceCtrl = function ($scope, $modalInstance) {

	$scope.close = function () {
		$modalInstance.close ();
	};

};

adaythere.controller ("adminCtrl", ["$scope", "$http", function ($scope, $http) {
	
	$scope.received_profile_data = [];
	$scope.received_days_data = [];
	$scope.profile_search_on = {};
	$scope.days_search_on = {};

	$scope.adminprofile_search = function () {
		var queried = false;
		var previous_param = false;
		var search_str = "";
		for (each in $scope.profile_search_on) {
			if ($scope.profile_search_on.hasOwnProperty (each)) {
				if (!queried) {
					queried = true;
					search_str += "?";
				}

				if (previous_param) {
					search_str += "&";
				} else {
					previous_param = true;
				}

				search_str += each;
				search_str += "=";
				search_str += escape ($scope.profile_search_on[each]);
			}
		}


		$http.get ("/admin_profiles" + search_str)
			.success (function (data, status, headers, config) {
				$scope.received_profile_data = data;
			}
		);
	};

	$scope.admindays_search = function () {
		var queried = false;
		var previous_param = false;
		var search_str = "";
		for (each in $scope.days_search_on) {
			if ($scope.days_search_on.hasOwnProperty (each)) {
				if (!queried) {
					queried = true;
					search_str += "?";
				}

				if (previous_param) {
					search_str += "&";
				} else {
					previous_param = true;
				}

				search_str += each;
				search_str += "=";
				search_str += escape ($scope.days_search_on[each]);
			}
		}


		$http.get ("/admin_days" + search_str)
			.success (function (data, status, headers, config) {
				$scope.received_days_data = data;
			}
		);
	};

	$scope.admindays_delete_day = function (day) {
		
		$http.post ("/admin_days", JSON.stringify (day))
			.success (function (data, status) {
				console.log ("delete day succeeded: " + status);	
			})
	       		.error (function (data, status) {
				console.log ("delete day failed: " + status);
			}
		);	
	}

	$scope.save_changed_user = function (user, msg_div) {
		$(msg_div).text ("");
		if ((user.name.length < 4) || (!test_name_characters (user.name))) {
			$(msg_div).text ("Invalid format for user name");
			return;
		}

		console.log (user);	
	
	};

	$scope.adminprofile_ban = function (user, ban) {
		user.banned = ban;
		
		$http.post ("/admin_profiles?type=ban", JSON.stringify (user))
			.success (function (data, status) {
				console.log ("post ban succeeded: " + status);	
			})
	       		.error (function (data, status) {
				console.log ("post ban failed: " + status);
				user.banned = !ban;
			}
		);	
	}

	$scope.adminprofile_change_ban = function (user) {
		user.banned = !user.banned;
	}
}]);

adaythere.controller ("profileCtrl", ["$scope", "$modal", "$http", "$compile", "profileService", "localityDaysService", function ($scope, $modal, $http, $compile, profileService, localityDaysService) {

	$scope.profile_body_content = { "error": "no profile" };

	$scope.become_a_contributor = function () {
		$scope.open_contribute_modal ();
	};

	$scope.open_contribute_modal = function () {

		var modalInstance = $modal.open ({
			templateUrl: 'becomeAContributorModalContent.html',
		    	controller: adaythere.BecomeAContributorModalInstanceCtrl,
		    	resolve: {
		    		$http: function () {
					return $http;
				}
			},
		    	scope: $scope,
		});

		modalInstance.result.then (function (data) {
			profileService.add_tool_access (data).then (function (result) {
				if (result) {
					$("#profile_ctrl_menu_toggle").text (result.name);
				       	$("#tool_user_related_menu").html ($compile(result.menu)($scope));

					ADT_SidebarDisplayControlInstance.display_control = true;
					$scope.gotoToolsPage();
				}
			});
		}, function () {
			console.log ('Modal dismissed at: ' + new Date ());
		});
	};

	$scope.profile = function () {

		profileService.getUserProfile ().then (function (data) {
			$scope.profile_body_content = data;

			var modalInstance = $modal.open ({
				templateUrl: 'profileModalContent.html',
			    	controller: adaythere.ProfileModalInstanceCtrl,
			    	resolve: {
				    	profile_body_content: function () {
					    	return $scope.profile_body_content;
				    	}	
			    	},
			    	scope: $scope 
			});

			modalInstance.result.then (function (selectedItem) {
				$scope.selected = selectedItem;
			}, function () {
				console.log ('Modal dismissed at: ' + new Date ());
			});

		}, function (data, status) {
			console.error (status, data);
		});

	};

	$scope.gotoToolsPage = function () {
		$("#welcome_to_left").hide ("slow");
		$("#welcome_to_right").hide ("slow");
		$("#daysearch_overlay").slideUp ();
 		ADT_SidebarDisplayControlInstance.display_control = true;
                $("#find_a_day").slideUp ("slow");
	};

	$scope.gotoSearchPage = function () {
		ADT_SidebarDisplayControlInstance.display_control = false;
		$("#find_a_day").slideDown ("fast");
		$("#welcome_to_left").show ("fast");
		$("#welcome_to_right").show ("fast");
		$("#daysearch_overlay").slideDown ();

		localityDaysService.getKeywords ();
	};
}]);

function test_name_characters (name) {
	var pattern = /^[a-z0-9_]+$/i;
	return pattern.test (name);
}

adaythere.directive ('contributorUserName', ['$http', function($http) {

	return function (scope, element, attrs) {
		var warn_el = "#" + attrs.warningId;
		element.blur (function () {
			$(warn_el).text (element[0].value);
		});

		element.keyup (function (ev) {
			var name = element[0].value;
			$(warn_el).text (name);
			if (!test_name_characters (name)) {
				$(warn_el).text (element[0].value + "contains characters that aren't permitted");
				return;
			}
		       		
			if (name.length >= 4) {
				
				$http.get ('/users?name='+name).success (function (data, status, headers, config) {
					$(warn_el).text (element[0].value + ' is ' + data);
				}).error (function (data, status, headers, config) {
					console.error (status, data);	
				});
			} 

		});			
	};
}]);

adaythere.BecomeAContributorModalInstanceCtrl = function ($scope, $modalInstance, $http) {


	$scope.contribute_modal_ok = function () {
		console.log ("contributor_modal_ok");
	
		var name = $("#contribute_google_nickname").val ();
		if (!name || name.length < 4 || !test_name_characters (name)) {
			console.error ("Invalid name", name);
			return;
		}

		console.log ($modalInstance);
		$http.post ("/users?name="+name).success (function (data, status, headers, config) {
				$modalInstance.close (data);
			}).error (function (data, status, headers, config) {
				console.error (status, data);
			});

	};

	$scope.contribute_modal_cancel = function () {
		$modalInstance.dismiss ('cancel');
	};
};

adaythere.ProfileModalInstanceCtrl = function ($scope, $modalInstance, profile_body_content) {

	$scope.profile_body_content = profile_body_content;

	$scope.selected = {
		profile_body_content: $scope.profile_body_content
	};
	
	$scope.ok = function () {
		$modalInstance.close ($scope.selected.profile_body_content);
	};

	$scope.cancel = function () {
		$modalInstance.dismiss ('cancel');
	};
};

function ADT_SidebarDisplayControl () {
	this.map_width = "70%";
	this.section_width = "30%"
	this.display_state = $("#sidebar_section").is (":visible") ? "Hide Tools" : "Show Tools";
	this.scope = null;
	this.mapService = null;
	this.current_zoom = ADT_Constants.DEFAULT_MAP_ZOOM;
	this.display_control = !$("#find_a_day").is (":visible");
}

ADT_SidebarDisplayControl.prototype.toggle_sidebar = function () {
	var visible = $("#sidebar_section").is (":visible");
	
	this.show_sidebar (!visible);
}

ADT_SidebarDisplayControl.prototype.set_scope = function (scope) {
	this.scope = scope;
}

ADT_SidebarDisplayControl.prototype.set_map = function (map) {

	if (!map) {
		console.log ("map not init");
	}
        this.mapService = map;
}

ADT_SidebarDisplayControl.prototype.show_sidebar = function (display) {

	var map = this.mapService.get ();

	if (map && $("#map_section").is (":visible")) {
		this.current_zoom = map.getZoom ();
	}

	if (display == false) {
		$("#map_section").css ("width", "100%");
		$("#map_section").show ();
		$("#sidebar_section").hide ();

	} else {
		if (this.at_minimum ()) {
			$("#sidebar_section").css ("width", "100%");
			$("#map_section").hide ();
			$("#sidebar_section").show ();
		} else {
			$("#sidebar_section").css ("width", this.section_width);
			$("#map_section").css ("width", this.map_width);
			$("#sidebar_section").show ();
			$("#map_section").show ();
		}

	}

	if (this.scope) {
		var phase = this.scope.$root.$$phase;
		if (phase == '$apply' || phase == '$digest') {
			this.scope.sidebar_display.menu_text = $("#sidebar_section").is (":visible") ? "Hide Tools" : "Show Tools";
		} else {
			var self = this;
			this.scope.$apply (function () {
				self.scope.sidebar_display.menu_text = $("#sidebar_section").is (":visible") ? "Hide Tools" : "Show Tools";
			});
		}
	} 

	if (map) {
		map.setZoom (this.current_zoom);
	}
}

ADT_SidebarDisplayControl.prototype.at_minimum = function () {
        var width = $(window).width ();

	return width < ADT_Constants.MINIMUM_WINDOW_WIDTH;
}

var ADT_SidebarDisplayControlInstance = new ADT_SidebarDisplayControl ();

adaythere.controller ("sidebarDisplayCtrl", ["$scope", "googleMapService", function ($scope, googleMapService) {
	$scope.sidebar_link = {};
	$scope.sidebar_link.map_is_displayed = ADT_SidebarDisplayControlInstance.display_control;

	$scope.$watch (function () {
		return ADT_SidebarDisplayControlInstance.display_control;
	}, function (val) {
		$scope.sidebar_link.map_is_displayed = val;
	});

	ADT_SidebarDisplayControlInstance.set_scope ($scope);
	ADT_SidebarDisplayControlInstance.set_map (googleMapService);
	$scope.sidebar_display = {};
	$scope.sidebar_display.menu_text = ADT_SidebarDisplayControlInstance.display_state;


	$scope.toggle_sidebar = function () {
		ADT_SidebarDisplayControlInstance.toggle_sidebar ();
	};
}]);

function ADT_Markers (map) {
	this.markers = [];
	this.map = map;
}


ADT_Markers.prototype.clear_all_markers = function () {
	for (var index in this.markers) {
		var marker = this.markers[index].marker;
		marker.setMap (null);
	}
	
	this.markers = [];	
};

ADT_Markers.prototype.remove_marker = function (marker) {
	marker.marker.setMap (null);
	var new_markers = [];

	for (var index in this.markers) {
		if (marker != this.markers[index]) {
			new_markers.push (this.markers[index]);
		}
	}

	this.markers = new_markers;
};

var ADAYTHERE_TYPES_ARRAY = [
	"airport",
	"amusement_park",
	"aquarium",
	"art_gallery",
	"bakery",
	"bank",
	"bar",
	"beauty_salon",
	"bicycle_store",
	"book_store",
	"bowling_alley",
	"bus_station",
	"cafe",
	"campground",
	"car_rental",
	"casino",
	"cemetery",
	"church",
	"city_hall",
	"clothing_store",
	"courthouse",
	"department_store",
	"electronics_store",
	"embassy",
	"fire_station",
	"florist",
	"food",
	"furniture_store",
	"grocery_or_supermarket",
	"gym",
	"hair_care",
	"hardware_store",
	"health",
	"hindu_temple",
	"home_goods_store",
	"hospital",
	"jewelry_store",
	"library",
	"liquor_store",
	"local_government_office",
	"lodging",
	"meal_delivery",
	"meal_takeaway",
	"mosque",
	"movie_rental",
	"movie_theater",
	"museum",
	"night_club",
	"painter",
	"park",
	"pet_store",
	"pharmacy",
	"physiotherapist",
	"place_of_worship",
	"post_office",
	"restaurant",
	"rv_park",
	"school",
	"shoe_store",
	"shopping_mall",
	"spa",
	"stadium",
	"store",
	"subway_station",
	"synagogue",
	"taxi_stand",
	"train_station",
	"university",
	"zoo"
];

adaythere.controller ("sidebarCtrl", ["$scope", "$modal", "$http", "$compile", 
		"googleMapService", "profileService", "userDaysService", "photoService", "localityDaysService",
		function ($scope, $modal, $http, $compile, googleMapService, profileService, userDaysService, photoService, localityDaysService) {

	$scope.location = googleMapService.location;
	$scope.clicked = googleMapService.clicked;

	$scope.my_days = userDaysService.user_days;
	$scope.my_deleted_days = userDaysService.deleted_days;

	$scope.current_created_day = new ADT_CreatedDay ();

	$scope.adt_markers = null

	$scope.adt_marker_modal = null

	googleMapService.initialize ($scope).then (function (geoloc) {
		googleMapService.clicked = geoloc.location;
		userDaysService.getDays ();
		$scope.current_created_day.full_locality = $scope.location.full_locality;
		$scope.adt_markers = new ADT_Markers (googleMapService.get ());
		$scope.adt_marker_modal = new ADT_MarkerModal ($scope, googleMapService.get (), $modal);
	});

	$scope.types = ADAYTHERE_TYPES_ARRAY;

	$scope.search = { selected_type: "all" };

	$scope.top_places_list = function (place) {
		return $scope.current_created_day.top_places_list (place);
	};

        $scope.bottom_places_list = function (place) {
		return $scope.current_created_day.bottom_places_list (place);
        };

	$scope.centre_map_at = function () {
		var address = $("#autocomplete_google_input").val ();
		googleMapService.geocoder.geocode ( { "address": address }, function (results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				$scope.current_created_day.full_locality = googleMapService.location.full_locality;
			} else {
				console.error ("Geocode was not successful for the following reason: " + status);
			}
		});
	};

	$scope.make_default_location = function () {
		profileService.setUserLocation ($scope.location);
	}

	$scope.places_array = [];

	$scope.search_places = function () {

		var sel_types = [];
		if (!$scope.search.selected_type || $scope.search.selected_type == "all") {
			sel_types = $scope.types;
		} else {
			sel_types.push ($scope.search.selected_type);
		}	

		var request = {
			location: new google.maps.LatLng (googleMapService.clicked.latitude, googleMapService.clicked.longitude),
			radius: googleMapService.boundsCircle.getRadius ()
		};


		request.types = sel_types;

		$scope.places_array = [];

		googleMapService.placesService.nearbySearch (request, function (results, status) {
			var pa = [];
			if (status == google.maps.places.PlacesServiceStatus.OK) {
				for (var i = 0; i < results.length; i++) {
					var place = results[i];
					pa.push (place);
				}
			}

			$scope.$apply (function () { $scope.places_array = pa; });
		});

	};

	$scope.show_search_area = function () {
		googleMapService.search_area_is_visible = !googleMapService.search_area_is_visible;
		googleMapService.boundsCircle.updateStatus (googleMapService.search_area_is_visible);	
	};



	$scope.set_marker_at_place = function (location) {
		var place = new ADT_Place ();
		
		if (location.types) {
			for (var i = 0; i < location.types.length; ++i) {
				place.types.push (location.types[i]);
			}	
		}
			
		if (location.geometry) {
			place.location.latitude = location.geometry.location.lat ();
			place.location.longitude = location.geometry.location.lng ();
		} else {
			place.location.latitude = location.latitude;
			place.location.longitude = location.longitude;
		}

		if (!location.name) { 
			place.name = $("#autocomplete_google_input").val () == "" ? "unknown" : $("#autocomplete_google_input").val ();
		} else {
			place.name = location.name;
		}
		
		place.vicinity = location.vicinity;
		place.comment = location.comment ? location.comment : "";

		for (var index in $scope.adt_markers.markers) {
			if (($scope.adt_markers.markers[index].location.latitude == place.location.latitude)
					&& ($scope.adt_markers.markers[index].location.longitude == place.location.longitude)) {
				return;
			}
		}

		for (var index in $scope.current_created_day.places) {
			var saved_place = $scope.current_created_day.places[index];
			if (place.equals (saved_place)) {
				return;
			}
		}

		place.marker = new google.maps.Marker ({
			position: new google.maps.LatLng (place.location.latitude, place.location.longitude),
		    	map: googleMapService.get ()
		});

		google.maps.event.addListener (place.marker, "click", function () {
			$scope.adt_marker_modal.open_marker_modal (place, true, true)

		});
	
		$scope.adt_markers.markers.push (place);
	};

	$scope.creation_remove = function (place) {
		$scope.current_created_day.remove (place);
	};

	$scope.creation_moveup = function (place) {
		$scope.current_created_day.moveup (place);
	};

	$scope.creation_movedown = function (place) {
		$scope.current_created_day.movedown (place);
	};


	$scope.find_a_day = {
		active: false
	};

	$scope.creation_save = function () {
		var ok = true;

		var title = ADT_string_trim ($scope.current_created_day.title);
		if (title == "") {
			var creation_title = $("#creation_title");
			var pre_border = creation_title.css ("border-color");
			creation_title.css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			creation_title.val ("Title required");
			creation_title.focus (function () {
				$scope.creation_title_exists = false;
				creation_title.val ("");
				creation_title.css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		var keywords = ADT_string_trim ($scope.current_created_day.keywords);
		if (keywords == "") {
			var creation_keywords = $("#creation_keywords");
			var pre_border = creation_keywords.css ("border-color");
			creation_keywords.css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			creation_keywords.val ("Comment required");
			creation_keywords.focus (function () {
				creation_keywords.val ("");
				creation_keywords.css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		var description = ADT_string_trim ($scope.current_created_day.description);
		if (description == "") {
			var creation_descrip = $("#creation_descrip");
			var pre_border = creation_descrip.css ("border-color");
			creation_descrip.css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			creation_descrip.val ("Comment required");
			creation_descrip.focus (function () {
				creation_descrip.val ("");
				creation_descrip.css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		if (ok) {
			for (var index in $scope.my_days) {
				if ($scope.current_created_day.title == $scope.my_days[index].title) {
					var creation_title = $("#creation_title");
					var pre_border = creation_title.css ("border-color");
					creation_title.css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
					var used_title = creation_title.val ();
					creation_title.val (used_title + " (Title already exists)");
					creation_title.focus (function () {
						$scope.creation_title_exists = false;
						creation_title.val (used_title);
						creation_title.css ({ "text-shadow": "none", "border-color": pre_border });
					});

					return;
				}
			}

			$scope.current_created_day.full_locality = $scope.location.full_locality;

			userDaysService.addDay ($scope.current_created_day);

			$scope.creation_clear ();
			$scope.find_a_day.active = true;

			$scope.tmp_photo_storage.saved = true;
		}

	};

	
	$scope.creation_day_display_pic = function (stored_pic) {
		var image = new Image ();
		image.src = "/photos?action=img&title=" + stored_pic;
		$("#creation_photo_" + stored_pic).append (image);

	};

	$scope.my_days_expand = function () {
		var is_collapsed = $("#my_days_expander").val () == "Collapse All";
		if (is_collapsed) {
			for (var each in $scope.my_days) {
				$scope.my_days[each].is_collapsed = true;
			}
			$("#my_days_expander").val ("Expand All");
			$scope.my_days_is_expanded = false;
		} else {

			for (var each in $scope.my_days) {
				$scope.my_days[each].is_collapsed = false;
			}
			$("#my_days_expander").val ("Collapse All");
			$scope.my_days_is_expanded = true;
		}
	};

	$scope.my_deleted_days_expand = function () {
		var is_collapsed = $("#my_deleted_days_expander").val () == "Collapse All";
		if (is_collapsed) {
			for (var each in $scope.my_deleted_days) {
				$scope.my_deleted_days[each].is_collapsed = true;
			}
			$("#my_deleted_days_expander").val ("Expand All");
			$scope.my_deleted_days_is_expanded = false;
		} else {

			for (var each in $scope.my_deleted_days) {
				$scope.my_deleted_days[each].is_collapsed = false;
			}
			$("#my_deleted_days_expander").val ("Collapse All");
			$scope.my_deleted_days_is_expanded = true;
		}
	};

	$scope.restore_day = function (day) {
		userDaysService.addDay (day);
		userDaysService.removeDeletedDay (day);
	};

	$scope.route_buttons = [];

	var route_displayed = false;
	var displayed_txt = "Hide";
	var hid_txt = "Display";
	$scope.hide_all_markers = function (index) {
		for (var i in $scope.route_buttons) {
			if (i == index) continue;
		
			if ($scope.route_buttons[i]) {
				$scope.remove_day_view_markers ($scope.my_days[i]);
				$scope.route_buttons[i] = false;
				var the_button_name = "#display_day_view_button_" + i;
				$(the_button_name).val (hid_txt);
				googleMapService.directionsRenderer.hideDirections ();
				route_displayed = false;
			}
		}
	};

	$scope.show_route_buttons = function (index) {
		if (!$scope.route_buttons[index]) {
			$scope.route_buttons[index] = false;
		}
		
		return $scope.route_buttons[index];
	}

	$scope.display_day_view = function (day, index) {
		var button_name = "#display_day_view_button_" + index;
		$scope.hide_all_markers (index);

		var is_displayed = ($(button_name).val () == displayed_txt);
		$scope.route_buttons[index] = !is_displayed;

		if (is_displayed) {
			$scope.remove_day_view_markers (day);
			googleMapService.directionsRenderer.hideDirections ();
			route_displayed = false;
			$(button_name).val (hid_txt);
		} else {
			$scope.set_day_markers (day);
			var len = day.places.length;
			var pos = 0;
		
			$(button_name).val (displayed_txt);
		}

	};

	$scope.direction_modes = [
		"Driving",
                "Walking",
		"Bicycling"
	];

	$scope.direction_mode = [];

	$scope.display_route = function (day, index) {

		if (route_displayed) {
			googleMapService.directionsRenderer.hideDirections ();
			route_displayed = false;
		} else {
			var mode;
			switch ($scope.direction_mode[index]) {
				case "Driving":
					mode = google.maps.TravelMode.DRIVING;
				       	break;
				case "Walking":
					mode = google.maps.TravelMode.WALKING;
					break;
				case "Bicycling":
					mode = google.maps.TravelMode.BICYCLING;
					break;
				default:
					mode = google.maps.TravelMode.DRIVING;
					break;	
			}
			googleMapService.directionsRenderer.showDirections (day, mode);
			route_displayed = true;
		}
	}

	$scope.day_displayed = function (day) {
		return day.is_displayed;
	};

	$scope.set_day_markers = function (day) {
		day.show_markers ($scope, googleMapService.get ());
	};

	$scope.remove_day_view_markers = function (day) {
		day.hide_markers ();		
	};

	$scope.tmp_photo_storage = {
		saved: true
	};

	$scope.creation_clear = function (delete_photos) {
		
		if (delete_photos) {
			var titles = [];
			for (var i = 0; i < $scope.current_created_day.photos.length; ++i) {
				titles.push ($scope.current_created_day.photos[i].title);
			}

			photoService.deleteTitles (titles);

			$scope.photo_storage.count = $scope.tmp_photo_storage.count;
			$scope.photo_storage.total_allowed = $scope.tmp_photo_storage.total_allowed;
			 
		}

		$scope.current_created_day.clear ();
		$scope.creation_alerts = [];
	};

	$scope.photo_storage = {
		count: photoService.current_count,
		total_allowed: photoService.total_allowed_photos
	};


	$scope.open_add_photo_modal = function () {
		
		if ($scope.tmp_photo_storage.saved) {
			$scope.tmp_photo_storage.count = $scope.photo_storage.count;
			$scope.tmp_photo_storage.total_allowed = $scope.photo_storage.total_allowed;
			$scope.tmp_photo_storage.saved = false;
		}

		var modalInstance = $modal.open ({
			templateUrl: 'addPhotosModalContent.html',
	    		controller: adaythere.AddPhotosModalInstanceCtrl,
	    		scope: $scope,
		    	compile: $compile,
		    	photoService: photoService
		});

		modalInstance.result.then (function (selections) {
			if (!selections) {
				return;
			}

			for (var i = 0; i <  selections.length; ++i) {
				var photo = new ADT_DayPhoto ();
				photo.title = selections[i];
				photo.description = "";
				$scope.current_created_day.photos.push (photo);
			}

		}, function () {
			console.log ('Modal dismissed at: ' + new Date ());
		});
	};

	$scope.edit_saved_day = function (day) {
		$scope.current_created_day = day;
		for (var index in $scope.current_created_day.places) {
			$scope.current_created_day.places[index].marker.setMap (googleMapService.get ());
		}
	};

	$scope.creation_close_alert = function (index) {
		$scope.alerts.splice (index, 1);
	};

	$scope.my_day_toggle_open = function (day) {
		day.is_collapsed = !day.is_collapsed;
	};

	$scope.day_is_editable = function (day) {
		return day.is_editable;
	};


	$scope.backup_copy_of_day = {};
	$scope.set_day_editable = function (day, index) {

		if (!$scope.current_created_day.is_cleared ()) {
			var rv = window.confirm ("Overwrite current unsaved day?");
			console.log (rv);
			if (rv) {
				$scope.current_created_day.clear ();
			} else {
				return;
			}
		}

		$scope.backup_copy_of_day[day.title] = ADT_CreatedDay.copy (day);

		$scope.display_day_view (day, index);

		day.is_editable = true;
		$scope.current_created_day = day;
		$("#creation_save_button").attr ("disabled", true);
		$("#creation_clear_button").attr ("disabled", true);
		$("#creation_photo_button").attr ("disabled", false);
		$("#creation_title").attr ("disabled", true);
	};

	$scope.cancel_changes_to_day = function (day) {

		$scope.hide_all_markers ();
		
		day.is_editable = false;
		day.keywords = $scope.backup_copy_of_day[day.title].keywords;
		day.description = $scope.backup_copy_of_day[day.title].description;
		day.places = $scope.backup_copy_of_day[day.title].places;
		
		$scope.current_created_day = new ADT_CreatedDay ();
		
		$("#creation_save_button").attr ("disabled", false);
		$("#creation_clear_button").attr ("disabled", false);
		$("#creation_photo_button").attr ("disabled", false);
		$("#creation_title").attr ("disabled", false);
	};


	$scope.save_modified_day = function (day) {
		userDaysService.updateDay (day);
		day.is_editable = false;

		$scope.current_created_day = ADT_CreatedDay.copy (day);

		$scope.hide_all_markers ();
		$scope.creation_clear ();

		$("#creation_save_button").attr ("disabled", false);
		$("#creation_clear_button").attr ("disabled", false);
		$("#creation_photo_button").attr ("disabled", false);
		$("#creation_title").attr ("disabled", false);
	};

	$scope.copy_day_as = function (day) {
		var rv = window.prompt ("Choose a new title", day.title);
		var new_title = ADT_string_trim (rv);

		for (i in $scope.my_days) {
			if ($scope.my_days[i].title == new_title) {
				window.alert ("You are already using " + new_title);
				return;
			}
		}

		new_day = ADT_shallow_copy (day);
		new_day.places = [];

		for (var each in day.places) {
			new_day.places[each] = ADT_shallow_copy (day.places[each]);
		}
		
		new_day.title = new_title;

		userDaysService.addDay (new_day);
	};

	$scope.delete_day = function (day) {
		var rv = window.confirm ("Delete day " + day.title + "?");

		if (rv) {
			userDaysService.deleteDay (day).then (function () {
				//localityDaysService.getKeywords ();
			});
		}
	};
}]);

adaythere.AddPhotosModalInstanceCtrl = function ($scope, $modalInstance, $compile, photoService) {

	$scope.collapsed = {};
	$scope.selections = {};

	var list = null;

	$scope.open_file_selection = function () {
		setTimeout(function() {
			$("#open_file_selection").click ();
		}, 0);		
	}

	$scope.file_selection = function (element) {
		var files = element.files;
		var available_count = photoService.total_allowed_photos - photoService.current_count;

		var length = files.length > available_count ? available_count : files.length;

		if (length > 0 && list == null) {
			list = $("<ul></ul>");			
			$("#pic_loader_div").append (list);
		}


		for (var i = 0; i < length; ++i) {
			var file = files[i];
			var name = file.name;
				
			var url = window.URL.createObjectURL (file);
			var img = new Image ();

			img.onload = function (evt) {
				var factor;

				if (this.width > this.height) {
					factor = 350 / this.naturalWidth;
				} else {
					factor = 350 / this.naturalHeight;
				}

				this.height = factor * this.naturalHeight;
			        this.width = factor * this.naturalWidth;
			};

			img.src = url;
			var item = $("<li></li");
			item.append (img);
			item.append (
				'<input type="text" class="pic_loader_title" value="' + name.split (".")[0] + '" />'
				+ '<input type="checkbox" class="pic_loader_action_checkbox" checked />'
			);
			list.append (item);
		}

	};

	$scope.upload_checked_photos = function () {
		var items = $("#pic_loader_div").children ("ul").children ("li");
		var selected_for_upload = [];
		var selections = []
		for (var i = 0; i < items.length; ++i) {
			var li = $(items[i]);
			var checkbox = $(li.children ('.pic_loader_action_checkbox')[0]);
			var title =  $(li.children ('.pic_loader_title')[0]).val ();

			var title_exists = false;

			for (var j = 0; j < photoService.title_list.length; ++j) {
				if (photoService.title_list[j] == title) {
					title_exists = true;
					break;
				}
			}

			if (title == "" || title_exists) {
				continue;				
			}



			if (checkbox.is (':checked')) {
				var img = $(li.children ('img')[0]).get (0);
				var canvas = document.createElement ("canvas");
				canvas.width = img.width;
				canvas.height = img.height;
				var ctx = canvas.getContext ("2d");
				ctx.drawImage (img, 0, 0, img.width, img.height);
				var storage_obj = {
					url: canvas.toDataURL ("image/png").replace ("data:image/png;base64,", ""),
					title: title
				};

				selected_for_upload.push (storage_obj);
				li.remove ();

				selections.push (title);
			}

		}

		photoService.upload (selected_for_upload).then (function () {
 			$scope.photo_storage.count = photoService.current_count;
              		$scope.photo_storage.total_allowed = photoService.total_allowed_photos;
               		$scope.photo_storage.available_files = photoService.title_list;
			$modalInstance.close (selections);
			
		});
	};

	$scope.remove_checked_photos = function () {
		var items = $("#pic_loader_div").children ("ul").children ("li");

		for (var i = 0; i < items.length; ++i) {
			var li = $(items[i]);
			var checkbox = $(li.children ('.pic_loader_action_checkbox')[0]);
			if (checkbox.is (':checked')) {
				var img = $(li.children ('img')[0]);
				li.remove ();
			}

		}

	};
	
	$scope.addphotos_modal_close = function () {
		$modalInstance.close ();
	};
};

function ADT_MarkerModal (scope, map, modal) {
	this.scope = scope;
	this.map = map;
	this.modal = modal;
}



ADT_MarkerModal.prototype.open_marker_modal = function (obj, show_add_button, arg) {
	this.scope.marker_content = obj;

	if (!this.scope.marker_content.vicinity) {
		if (this.scope.marker_content.location && this.scope.marker_content.location.vicinity) {
			this.scope.marker_content.vicinity = this.scope.marker_content.location.vicinity;
		}
	}

	this.scope.marker_content.is_editable = (typeof arg != 'undefined' &&  typeof arg.is_editable != "undefined") ? arg.is_editable : arg;

	var self = this;

	var modalInstance = this.modal.open ({
		templateUrl: 'markerModalContent.html',
	    	controller: adaythere.MarkerModalInstanceCtrl,
	    	resolve: {
			marker_content: function () {
				return self.scope.marker_content;
			},
	    		show_add_button: function () {
		    		return show_add_button;
	    		},
	    		map: function () {
		    		return self.map;
	    		}
	    	},
	    	scope: self.scope 
	});

	modalInstance.result.then (function (place) {
		if (place) {
			self.scope.current_created_day.places.push (place);
			var sep = "";
			if (self.scope.current_created_day.keywords.length > 0) {
				sep = ", ";
			}
			for (var i = 0; i < place.types.length; ++i) {

				if (place.types[i] == "establishment") {
					continue;
				}

				if (self.scope.current_created_day.keywords.indexOf (place.types[i]) > -1) {
					continue;
				}

				self.scope.current_created_day.keywords += sep;
				self.scope.current_created_day.keywords += place.types[i];
				sep = ", ";
			}
		}
	}, function () {

	});
};

adaythere.MarkerModalInstanceCtrl = function ($scope, $modalInstance, marker_content, show_add_button, map) {
	$scope.show_add_button = show_add_button;

	$scope.marker_content = marker_content;

	$scope.marker_modal_ok = function () {
		$modalInstance.close ();
	};

	$scope.marker_modal_cancel = function () {
		$modalInstance.dismiss ('cancel');
	};

	$scope.marker_modal_add_to_day = function (marker_content) {

		var place = ADT_Place.from_marker_content (marker_content);

		for (var index in $scope.current_created_day.places) {
			var saved_place = $scope.current_created_day.places[index];
			if (place.equals (saved_place)) {
				return;
			}

		}

		if (place.types.length == 0) {
			place.types[0] = "other";
		}

		$scope.adt_markers.remove_marker (marker_content);

		place.marker = new google.maps.Marker ({
			position: new google.maps.LatLng (place.location.latitude, place.location.longitude),
			map: map
		});

		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'; 
		place.marker.setIcon (iconFile);

		google.maps.event.addListener (place.marker, "click", function () {
	        	$scope.adt_marker_modal.open_marker_modal (place, false, true);
	        });
		
		$modalInstance.close (place);
	};


};


/*
 * jquery callbacks
 */


var size_daysearch = function (w, h, small) {

	var overlay_width = small ? w : 600;
	$("#daysearch_overlay").css ({
		"position": "absolute",
		"width": overlay_width,
		"left": (w - overlay_width) / 2
	});


	var width = $(".fieldset_daysearch").width ();

	var max = 0;
	$(".daysearch_label").each(function(){
        	if ($(this).width() > max)
            	max = $(this).width();    
    	});
    	$(".daysearch_label").width(max);

	var input_width = $(".daysearch_input").width () - max;

       	$(".daysearch_input").width (input_width);	

	var overlay_height = $(".fieldset_daysearch").height ();
	var overlay_top = (h / 2) - overlay_height;
	$("#daysearch_overlay").css ("top", overlay_top);	


};

var size_daysearch_return = function (w, h, small) {
	if (small || ((w * 3)/5.0 < 900)) {
		$("#daysearch_return_display").css ("width", "100%");
	} else {
		$("#daysearch_return_display").css ("width", "60%");
		$("#daysearch_return_display").css ("margin-left", "auto");
		$("#daysearch_return_display").css ("margin-right", "auto");
	}

	$("#daysearch_return_display").css ("height", "80%");
}

$(window).resize (function () {

	var width = $(window).width ();
	var height = $(window).height ();

	size_daysearch (width, height, width < 900);
	size_daysearch_return (width, height, width < 900);

	if (width < 900) {
		ADT_SidebarDisplayControlInstance.show_sidebar (false);
	} else {
		ADT_SidebarDisplayControlInstance.show_sidebar (true);
	}

	ADT_set_section_height (height);
	
})


$(function () {

	var width = $(window).width ();
	var height = $(window).height ();

	size_daysearch (width, height, width < 900);
	size_daysearch_return (width, height, width < 900);

	if (width < 900) {
		ADT_SidebarDisplayControlInstance.show_sidebar (false);
	}	

	ADT_set_section_height (height);


});



