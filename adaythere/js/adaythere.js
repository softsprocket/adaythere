function ADT_set_element_positions (width, height) {

	var map_width = Math.floor(width * 0.7);
	var sidebar_width = Math.floor(width * 0.3); 
	$("#map_section").width (map_width);
	$("#sidebar_section").width (sidebar_width); 
}

function ADT_set_section_height (height) {
	var h1 = $("#page_header").height();
	var h2 = $("#page_footer").height();
	var val = height - (h1 + h2);
	$("#map_section").height(val);
	$("#sidebar_section").height(val);
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
	arr.splice (parseInt(index) + 1, 0, removed[0]);
}

function ADT_swap_with_prev (arr, index) {
	var removed = arr.splice (index, 1);
	arr.splice (parseInt(index) - 1, 0, removed[0]);
}

function ADT_string_trim (str) {
	return str.replace(/^\s+|\s+$/gm,'');
}


function ADT_DirectionsRenderer (map) {
	this.directionsService = new google.maps.DirectionsService();
	this.directionsDisplay = new google.maps.DirectionsRenderer();
	this.directionsDisplay.setOptions( { suppressMarkers: true } );

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
	this.directionsService.route(request, function(result, status) {
		if (status == google.maps.DirectionsStatus.OK) {
			self.directionsDisplay.setDirections(result);
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
			}
		}
	}

	return place;
}

function ADT_CreatedDay () {
	this.title = "";
	this.keywords = "";
	this.description = "";
	this.places = [];

	this.markers_visible = false;
}

ADT_CreatedDay.prototype.top_places_list = function (place) {
	return this.places[0].equals (place);
};

ADT_CreatedDay.prototype.bottom_places_list = function (place) {
	return this.places[this.places.length - 1].equals (place);
};

ADT_CreatedDay.prototype.swap_with_next = function (index) {
	var removed = this.places.splice (index, 1);
	this.places.splice (parseInt(index) + 1, 0, removed[0]);
}

ADT_CreatedDay.prototype.swap_with_prev = function (index) {
	var removed = this.places.splice (index, 1);
	this.places.splice (parseInt(index) - 1, 0, removed[0]);
}

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
	day.locality = this.locality;

	for (var index in this.places) {
		var place = new ADT_Place ();
        	place.name = this.places[index].name;
	        place.comment = this.places[index].comment;
		place.location.latitude = this.places[index].location.latitude;
		place.location.longitude = this.places[index].location.longitude;
		place.vicinity = this.places[index].vicinity;

		day.places.push (place);
	}

	return JSON.stringify (day);	
};

ADT_CreatedDay.prototype.show_markers = function (scope, map) {
	var markerBounds = new google.maps.LatLngBounds();

	var add_listener = function (marker, place) {
		google.maps.event.addListener (marker, "click", function () {
			scope.open_marker_modal (place, false, false);
		});

		var infowindow = new google.maps.InfoWindow({
			content: "<img src='https://imagizer.imageshack.us/v2/419x655q90/33/qx22.jpg' height='210' width='200'></img>"
		});

		google.maps.event.addListener(place.marker, 'mouseover', function() {
			infowindow.open(map, place.marker);
		});

	};

	for (var each in this.places) {
		var markerPosition = new google.maps.LatLng (this.places[each].location.latitude, this.places[each].location.longitude);
		this.places[each].marker = new google.maps.Marker({
			position: markerPosition,
			map: map
		});

		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
		this.places[each].marker.setIcon(iconFile);

		add_listener (this.places[each].marker, this.places[each]);

		markerBounds.extend(markerPosition);

	}

	map.fitBounds(markerBounds);

	this.markers_visible = true;
}

ADT_CreatedDay.prototype.hide_markers = function () {
	for (var each in this.places) {
		this.places[each].marker.setMap (null);
	}

	this.markers_visible = false;
}

ADT_CreatedDay.copy = function (created_day) {
	var day = new ADT_CreatedDay ();

	day.title = created_day.title;
	day.keywords = created_day.keywords;
	day.description = created_day.description;
	day.locality = created_day.locality;

	day.is_editable = created_day.is_editable;
	day.has_been_modified = created_day.has_been_modified;
	day.is_collapsed = created_day.is_collapsed;

	for (var index in created_day.places) {
		var place = new ADT_Place ();
		place.name = created_day.places[index].name;
		place.comment = created_day.places[index].comment;
		place.location.latitude = created_day.places[index].location.latitude;
		place.location.longitude = created_day.places[index].location.longitude;
		place.vicinity = created_day.places[index].vicinity;

		day.places.push (place);
	}

	return day;
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
		if (data && !isNaN(data.latitude)) {
			self.location.latitude = data.latitude;
			self.location.longitude = data.longitude;
			self.location.locality = data.locality;
			self.location.vicinity = data.address;
			self.default_location_set = true;
		} else {

			self.location.latitude = 48.422;
			self.location.longitude = -123.408;
			self.location.locality = "Victoria";
			self.location.vicinity = "Victoria, BC Canada";
		}
	}, function () {

		self.location.latitude = 48.422;
		self.location.longitude = -123.408;
		self.location.locality = "Victoria";
		self.location.vicinity = "Victoria, BC Canada";
	});
}

ADT_GeoLocate.prototype.geolocate = function () {
	var self = this;
	var deferred = $.Deferred ();

	this.setDefault().then (function () {
		if (self.default_location_set == true) {
			deferred.resolve();
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
	this.location.locality = data.locality ? data.locality : "";
	this.location.vicinity = data.vicinity ? data.vicinity : "";
}

ADT_GeoLocate.prototype.getLocation = function () {
	return this.location;
}

/*
 * ADT_GoogleMapService
 */
function ADT_GoogleMapService (location) {
	this.geoloc = new ADT_GeoLocate (location);
	this.geocoder = new google.maps.Geocoder();
	this.map = null;
	this.autocomplete = null;
	this.boundsCircle =null;
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
		console.error (err_msg);
	}).always (function () {
		var zoom = 12;

		var styles = [{
			featureType: "poi",
			elementType: "labels",
			stylers: [
				{ visibility: "off" }
			]		
		}];

		var mapOptions = {
			center: new google.maps.LatLng(self.geoloc.location.latitude, self.geoloc.location.longitude),
			zoom: zoom,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			styles: styles
		};

		var el = document.getElementById("map_section");
		self.map = new google.maps.Map(el, mapOptions);
		self.map.setOptions({styles: styles});
		self.placesService = new google.maps.places.PlacesService(self.map);

		var input = document.getElementById ("pac_input");
		var div = document.getElementById ("search_util");

		self.autocomplete = new google.maps.places.Autocomplete(input);
		self.autocomplete.bindTo("bounds", self.map);

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

		self.boundsCircle = new ADT_BoundingCircle (self.map);

		google.maps.event.addListener(self.map, 'bounds_changed', function() {
			self.boundsCircle.updateBounds (self.map.getBounds());
			self.boundsCircle.updateStatus (self.search_area_is_visible);
		});


		google.maps.event.addListener (self.map, "click", function (event) {
		       	self.set_search_location (event, scope);
		});
		
		self.boundsCircle.addClickListener (function (event) {
			self.set_search_location (event, scope);
		});

		google.maps.event.addListener (self.map, "dblclick", function(event) {
			window.clearTimeout (self.timerId);
		});
		
		google.maps.event.addListener (self.map, "center_changed", function() {
			var latlng = self.map.getCenter();
			self.location.latitude = latlng.lat ();
			self.location.longitude = latlng.lng ();

			self.moved = true;


			//scope.$apply (function () {
				self.clicked = self.location;
			//});

		});

		google.maps.event.addListener (self.map, "mouseup", function() {
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

		google.maps.event.addListener (self.autocomplete, "place_changed", function() {
			
			var place = self.autocomplete.getPlace();
			self.placeChange (place);
		});


		self.directionsRenderer = new ADT_DirectionsRenderer (self.map);
	});

	return deferred;
}

ADT_GoogleMapService.prototype.get = function () {
	return this.map;
}

ADT_GoogleMapService.prototype.placeChange = function (place) {

	if (!place.geometry) {
		return;
	}

	if (place.geometry.viewport) {
		this.map.fitBounds(place.geometry.viewport);
	} else {
		this.map.setCenter(place.geometry.location);
	}

	var locality = ADT_getLocality (place.address_components);
	var vicinity = place.formatted_address;

	self.geoloc.setRegion ({locality: locality, vicinity: vicinity});

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
var adaythere = angular.module("adaythere", ['ui.bootstrap']);

adaythere.factory ("googleMapService", [ "profileService", function (profileService) {
	return new ADT_GoogleMapService (profileService.getLocation());
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

	this.getUserProfile ().then(function (data) {
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
		this.$http({
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

	this.$http({
		method: "POST",
		url: "/profile",
		data: { location: location }
	}).success (function (data, status, headers, config) {
		self.profile_data = data;
	}).error (function (data, status, headers, config) {
		console.error (status, data);
	});

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
}

ADT_UserDaysService.prototype.getDays = function () {
	var deferred = this.$q.defer ();
	var self = this;

	if (this.user_days.length > 0) {
		deferred.resolve (this.user_days);
	} else {
		this.$http.get ("/places").success (function (data, status, headers, config) {
			for (var each in data) {
				var day = JSON.parse (data[each]);
				day.is_editable = false;
				day.has_been_modified = false;
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
	this.$http.put("/places", day.to_json ()).success (function (data, status, headers, config) {
		day.is_collapsed = false;
		for (var index in self.user_days) {
			self.user_days[index].is_collapsed = true;
		}

		day.is_editable = false;
		day.has_been_modified = false;
		
		self.user_days.push (day);

	}).error (function (data, status, headers, config) {
		console.error (status, data);
	});
}

adaythere.factory ("userDaysService", ["$http", "$q", function ($http, $q) {
	return new ADT_UserDaysService ($http, $q);
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
	var sw = bounds.getSouthWest();
	var ctr = bounds.getCenter();
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
	var diff = google.maps.geometry.spherical.computeDistanceBetween(left, ctr);

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

	this.boundsCircle = new google.maps.Circle(this.circleOptions);
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

adaythere.controller ("loginCtrl", ["$scope", "$http", function ($scope, $http) {

	$scope.googlelogin = function () {
		$http.get ("/login?method=google")
			.success (function(data, status, headers, config) {
				window.location.href = data.url;
			}
		);
	};
	
	$scope.googlelogout = function () {
		$http.get ("/logout?method=google")
			.success (function(data, status, headers, config) {
				window.location.href = data.url;
			}
		);
	};
}]);

adaythere.controller ("adminCtrl", ["$scope", "$http", "$modal", function ($scope, $http, $modal) {

	$scope.received_profile_data = [];

	$scope.admin_profiles = function () {
		$scope.modalInstance = $modal.open({
			templateUrl: 'adminProfileModalContent.html',
		    	controller: adaythere.AdminProfileModalInstanceCtrl,
		    	resolve: {
			    	received_profile_data: function () {
			    		return $scope.received_profile_data;
				}
			},
		    	scope: $scope
		});

		$scope.modalInstance.result.then(function () {

		}, function () {
			console.log ('Modal dismissed');
		});

	}

}]);

adaythere.AdminProfileModalInstanceCtrl = function ($scope, $modalInstance, $http, received_profile_data) {

	$scope.received_profile_data = received_profile_data;
	$scope.search_on = {};

	$scope.adminprofile_modal_ok = function () {
		var queried = false;
		var previous_param = false;
		var search_str = "";
		for (each in $scope.search_on) {
			if ($scope.search_on.hasOwnProperty (each)) {
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
				search_str += escape ($scope.search_on[each]);
			}
		}


		$http.get ("/admin_profiles" + search_str)
			.success (function(data, status, headers, config) {
				$scope.received_profile_data = data;
			}
		);
	};

	$scope.adminprofile_modal_cancel = function () {
		$modalInstance.dismiss('cancel');
	};

	$scope.adminprofile_modal_ban = function (user, ban) {
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

};

adaythere.controller ("profileCtrl", ["$scope", "$modal", "profileService", function ($scope, $modal, profileService) {

	$scope.profile_body_content = { "error":"no profile" };

	$scope.profile = function () {

		profileService.getUserProfile ().then (function (data) {
			$scope.profile_body_content = data;

			var modalInstance = $modal.open({
				templateUrl: 'profileModalContent.html',
			    	controller: adaythere.ProfileModalInstanceCtrl,
			    	resolve: {
				    	profile_body_content: function () {
					    	return $scope.profile_body_content;
				    	}	
			    	},
			    	scope: $scope 
			});

			modalInstance.result.then(function (selectedItem) {
				$scope.selected = selectedItem;
			}, function () {
				console.log ('Modal dismissed at: ' + new Date());
			});

		}, function (data, status) {
			console.error (status, data);
		});

	};

}]);

adaythere.ProfileModalInstanceCtrl = function ($scope, $modalInstance, profile_body_content) {

	$scope.profile_body_content = profile_body_content;

	$scope.selected = {
		profile_body_content: $scope.profile_body_content
	};
	
	$scope.ok = function () {
		$modalInstance.close($scope.selected.profile_body_content);
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
};



adaythere.controller ("sidebarCtrl", ["$scope", "$modal", "$http", "googleMapService", "profileService", "userDaysService", function (
			$scope, $modal, $http, googleMapService, profileService, userDaysService) {
	$scope.location = googleMapService.location;
	$scope.clicked = googleMapService.clicked;

	$scope.my_days = userDaysService.user_days;

	googleMapService.initialize ($scope).then (function (geoloc) {
		googleMapService.clicked = geoloc.location;
		userDaysService.getDays ();
	});

	$scope.types = [
		"amusement_park",
		"aquarium",
		"art_gallery",
		"bakery",
		"bar",
		"beauty_salon",
		"bicycle_store",
		"book_store",
		"bowling_alley",
		"cafe",
		"casino",
		"clothing_store",
		"florist",
		"food",
		"grocery_or_supermarket",
		"hair_care",
		"jewelry_store",
		"library",
		"movie_theater",
		"museum",
		"night_club",
		"park",
		"restaurant",
		"shoe_store",
		"shopping_mall",
		"spa",
		"stadium",
		"store",
		"zoo"
	];

	$scope.search = { selected_type: "all" };

	$scope.current_created_day = new ADT_CreatedDay ();

	$scope.top_places_list = function (place) {
		return $scope.current_created_day.top_places_list (place);
	};

        $scope.bottom_places_list = function (place) {
		return $scope.current_created_day.bottom_places_list (place);
        };

	$scope.centre_map_at = function () {
		var address = $("#pac_input").val ();
		googleMapService.geocoder.geocode( { "address": address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var place = results[0];
				googleMapService.placeChange ($scope, place);
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

		googleMapService.placesService.nearbySearch(request, function (results, status) {
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

	$scope.markers = [];

	$scope.clear_all_markers = function () {
		for (var index in $scope.markers) {
			var marker = $scope.markers[index].marker;
			marker.setMap (null);
		}
		$scope.markers = [];	
	};

	$scope.remove_marker = function (marker) {
		marker.marker.setMap (null);
		var new_markers = [];

		for (var index in $scope.markers) {
			if (marker != $scope.markers[index]) {
				new_markers.push ($scope.markers[index]);
			}
		}

		$scope.markers = new_markers;
	};


	$scope.open_marker_modal = function (obj, show_add_button, editable) {
		$scope.marker_content = obj;
		$scope.marker_content.is_editable = editable;
		
		var modalInstance = $modal.open({
			templateUrl: 'markerModalContent.html',
		    	controller: adaythere.MarkerModalInstanceCtrl,
		    	resolve: {
			    	marker_content: function () {
				    	return $scope.marker_content;
			    	},
		    		show_add_button: function () {
					return show_add_button;
				},
		    		map: function () {
					return googleMapService.get ();
				}
		    	},
		    	scope: $scope 
		});

		modalInstance.result.then(function (place) {
			if (place) {
				$scope.current_created_day.places.push (place);
			}
		}, function () {
		
		});
	};

	$scope.open_selectday_modal = function (obj) {
		$scope.marker_content = obj;

		var modalInstance = $modal.open({
			templateUrl: 'selectDayModalContent.html',
		    	controller: adaythere.SelectDayModalInstanceCtrl,
		    	resolve: {
			    	marker_content: function () {
				    	return $scope.marker_content;
			    	}
		    	},
		    	scope: $scope 
		});

		modalInstance.result.then(function (marker_content) {
			$scope.marker_content = marker_content;
		}, function () {
			console.log ('Modal dismissed at: ' + new Date());
		});
	};

	$scope.set_marker_at_place = function (location) {
		var place = new ADT_Place ();

		if (location.geometry) {
			place.location.latitude = location.geometry.location.lat ();
			place.location.longitude = location.geometry.location.lng ();
		} else {
			place.location.latitude = location.latitude;
			place.location.longitude = location.longitude;
		}

		if (!location.name) { 
			place.name = $("#pac_input").val() == "" ? "unknown" : $("#pac_input").val();
		} else {
			place.name = location.name;
		}
		
		place.vicinity = location.vicinity;
		place.comment = location.comment ? location.comment : "";

		for (var index in $scope.markers) {
			if (($scope.markers[index].location.latitude == place.location.latitude)
					&& ($scope.markers[index].location.longitude == place.location.longitude)) {
				return;
			}
		}

		for (var index in $scope.current_created_day.places) {
			var saved_place = $scope.current_created_day.places[index];
			if (place.equals (saved_place)) {
				return;
			}
		}

		place.marker = new google.maps.Marker({
			position: new google.maps.LatLng (place.location.latitude, place.location.longitude),
		    	map: googleMapService.get ()
		});

		
		google.maps.event.addListener (place.marker, "click", function () {
			$scope.open_marker_modal (place, true, true)

		});
		
		$scope.markers.push (place);
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
			var pre_border = $("#creation_title").css ("border-color");
			$("#creation_title").css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			$("#creation_title").val ("Title required");
			$("#creation_title").focus (function () {
				$scope.creation_title_exists = false;
				$("#creation_title").val ("");
				$("#creation_title").css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		var keywords = ADT_string_trim ($scope.current_created_day.keywords);
		if (keywords == "") {
			var pre_border = $("#creation_keywords").css ("border-color");
			$("#creation_keywords").css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			$("#creation_keywords").val ("Comment required");
			$("#creation_keywords").focus (function () {
				$("#creation_keywords").val ("");
				$("#creation_keywords").css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		var description = ADT_string_trim ($scope.current_created_day.description);
		if (description == "") {
			var pre_border = $("#creation_descrip").css ("border-color");
			$("#creation_descrip").css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
			$("#creation_descrip").val ("Comment required");
			$("#creation_descrip").focus (function () {
				$("#creation_descrip").val ("");
				$("#creation_descrip").css ({ "text-shadow": "none", "border-color": pre_border });
			});
			ok = false;
		}

		if (ok) {
			for (var index in $scope.my_days) {
				if ($scope.current_created_day.title == $scope.my_days[index].title) {
					var pre_border = $("#creation_title").css ("border-color");
					$("#creation_title").css ({ "text-shadow": "0 0 10px red", "border-color": "red" });
					var used_title = $("#creation_title").val ();
					$("#creation_title").val (used_title + " (Title already exists)");
					$("#creation_title").focus (function () {
						$scope.creation_title_exists = false;
						$("#creation_title").val (used_title);
						$("#creation_title").css ({ "text-shadow": "none", "border-color": pre_border });
					});

					return;
				}
			}

			$scope.current_created_day.locality = $scope.location.locality;

			userDaysService.addDay ($scope.current_created_day);

			$scope.creation_clear ();
			$scope.find_a_day.active = true;
		}

	};

	$scope.my_days_expand = function () {
		var is_collapsed = $("#my_days_expander").val() == "Collapse All";
		if (is_collapsed) {
			for (var each in $scope.my_days) {
				$scope.my_days[each].is_collapsed = true;
			}
			$("#my_days_expander").val("Expand All");
			$scope.my_days_is_expanded = false;
		} else {

			for (var each in $scope.my_days) {
				$scope.my_days[each].is_collapsed = false;
			}
			$("#my_days_expander").val("Collapse All");
			$scope.my_days_is_expanded = true;
		}
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
				$(the_button_name).val(hid_txt);
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

		var is_displayed = ($(button_name).val() == displayed_txt);
		$scope.route_buttons[index] = !is_displayed;

		if (is_displayed) {
			$scope.remove_day_view_markers (day);
			googleMapService.directionsRenderer.hideDirections ();
			route_displayed = false;
			$(button_name).val(hid_txt);
		} else {
			$scope.set_day_markers (day);
			var len = day.places.length;
			var pos = 0;
		
			console.log (displayed_txt);	
			$(button_name).val(displayed_txt);
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

	$scope.creation_clear = function () {
		$scope.current_created_day.title = "";
		$scope.current_created_day.description = "";
		$scope.current_created_day.keywords = "";
		$scope. creation_alerts = [];
		for (var index in $scope.current_created_day.places) {
			$scope.current_created_day.places[index].marker.setMap (null);
		}

		$scope.current_created_day.places = [];
	};

	$scope.edit_saved_day = function (day) {
		$scope.current_created_day = day;
		for (var index in $scope.current_created_day.places) {
			$scope.current_created_day.places[index].marker.setMap (googleMapService.get ());
		}
	};

	$scope.creation_close_alert = function (index) {
		$scope.alerts.splice(index, 1);
	};

	$scope.my_day_toggle_open = function (day) {
		day.is_collapsed = !day.is_collapsed;
	};

	$scope.day_is_editable = function (day) {
		return day.is_editable;
	};

	$scope.day_has_been_modified = function (day) {
		return day.has_been_modified;
	};

	$scope.backup_copy_of_day = {};
	$scope.set_day_editable = function (day) {
		$scope.backup_copy_of_day[day.title] = ADT_shallow_copy (day);
		$scope.backup_copy_of_day[day.title].places = [];

		for (var each in day.places) {
			$scope.backup_copy_of_day[day.title].places[each] = ADT_shallow_copy (day.places[each]);
		}

		day.is_editable = true;
	};

	$scope.cancel_changes_to_day = function (day) {
		day.is_editable = false;
		day.has_been_modified = false;
		day.keywords = $scope.backup_copy_of_day[day.title].keywords;
		day.description = $scope.backup_copy_of_day[day.title].description;
		day.places = $scope.backup_copy_of_day[day.title].places;
	};

}]);

adaythere.MarkerModalInstanceCtrl = function ($scope, $modalInstance, marker_content, show_add_button, map) {
	$scope.show_add_button = show_add_button;

	$scope.marker_content = marker_content;

	$scope.marker_modal_ok = function () {
		$modalInstance.close();
	};

	$scope.marker_modal_cancel = function () {
		$modalInstance.dismiss('cancel');
	};

	$scope.marker_modal_add_to_day = function (marker_content) {
		var place = ADT_Place.from_marker_content (marker_content);

		for (var index in $scope.current_created_day.places) {
			var saved_place = $scope.current_created_day.places[index];
			if (place.equals (saved_place)) {
				return;
			}
		}

		$scope.remove_marker(marker_content);

		place.marker = new google.maps.Marker({
			position: new google.maps.LatLng (place.location.latitude, place.location.longitude),
			map: map
		});

		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'; 
		place.marker.setIcon(iconFile);

		google.maps.event.addListener (place.marker, "click", function () {
	        	$scope.open_marker_modal (place, false, true);
	        });

		var infowindow = new google.maps.InfoWindow({
			content: "<img src='https://imagizer.imageshack.us/v2/419x655q90/33/qx22.jpg'></img>"
		});

		google.maps.event.addListener(place.marker, 'mouseover', function() {
			infowindow.open(map, place.marker);
		});

		$modalInstance.close(place);
	};
};

adaythere.SelectDayModalInstanceCtrl = function ($scope, $modalInstance, marker_content) {

	$scope.marker_content = marker_content;

	$scope.selectday_modal_ok = function () {
		$modalInstance.close($scope.marker_content);
	};

	$scope.selectday_modal_cancel = function () {
		$modalInstance.dismiss('cancel');
	};
};


/*
 * jquery callbacks
 */
$(window).resize (function () {
	var width = $(window).width();
	var height = $(window).height();

//	ADT_set_element_positions (width, height);

	ADT_set_section_height (height);
})


$(function () {

	var width = $(window).width();
	var height = $(window).height();
	
	ADT_set_section_height (height);
//	ADT_set_element_positions (width, height);

});


