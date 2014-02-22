function ADT_set_element_positions (width, height) {

	map_width = Math.floor(width * 0.7);
	sidebar_width = Math.floor(width * 0.3); 
	$("#map_section").width (map_width);
	$("#sidebar_section").width (sidebar_width); 
}

function ADT_set_section_height (height) {
	h1 = $("#page_header").height();
	h2 = $("#page_footer").height();
	val = height - (h1 + h2);
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
			console.log ("Data", data);
			self.location = data;
			self.default_location_set = true;
		} else {

			self.location.latitude = 48.422;
			self.location.longitude = -123.408;
			self.location.locality = "Victoria";
			self.location.address = "Victoria, BC Canada";
		}
	}, function () {

		self.location.latitude = 48.422;
		self.location.longitude = -123.408;
		self.location.locality = "Victoria";
		self.location.address = "Victoria, BC Canada";
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
var adaythere = angular.module("adaythere", ['ui.bootstrap']);

adaythere.factory('safeApply', [function($rootScope) {
	return function($scope, fn) {
		var phase = $scope.$root.$$phase;
		if(phase == '$apply' || phase == '$digest') {
			if (fn) {
				$scope.$eval(fn);
			}
		} else {
			if (fn) {
				$scope.$apply(fn);
			} else {
				$scope.$apply();
			}
		}
	}
}]);

/*
 * Create location service
 */
function ADT_LocationInitializerService (location) {
	this.geoloc = new ADT_GeoLocate (location);
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

		var input = document.getElementById ("pac_input");
		var div = document.getElementById ("search_util");

		self.autocomplete = new google.maps.places.Autocomplete(input);
		self.autocomplete.bindTo("bounds", self.map.get ());

		if (self.geoloc.location.address) {
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

adaythere.factory ("locationInitializer", [ "profileService", function (profileService) {
	return new ADT_LocationInitializerService (profileService.getLocation());
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

	console.log (location);
}

adaythere.factory ("profileService", ["$http", "$q", function ($http, $q) {
	return new ADT_ProfileService ($http, $q);
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
				console.log (selectedItem)
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



adaythere.controller ("sidebarCtrl", ["$scope", "$modal", "locationInitializer", "profileService", "safeApply", function (
			$scope, $modal, locationInitializer, profileService, safeApply) {
	$scope.location = locationInitializer.getLocation ();
	$scope.clicked = {
		latitude: "",
		longitude: "",
		locality: "",
		address: ""
	}


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

	$scope.current_creation_day = {
		title: "",
		description: "",
		places: []
	};

	$scope.not_top_places_list = function (place) {
		return $scope.current_creation_day.places[0] != place;
	};

        $scope.not_bottom_places_list = function (place) {
		return $scope.current_creation_day.places[$scope.current_creation_day.places.length - 1] != place;
        };


	var boundsCircle;
	var search_area_is_visible = false;

	locationInitializer.initialize ().then (function (geoloc) {
		safeApply($scope, function () {
			$scope.location = geoloc.location;
			$scope.clicked = $scope.location;
		});

		var moved = false;
		boundsCircle = new ADT_BoundingCircle (locationInitializer.map.get ());

		google.maps.event.addListener(locationInitializer.map.get (), 'bounds_changed', function() {
			boundsCircle.updateBounds (locationInitializer.map.get ().getBounds());
			boundsCircle.updateStatus (search_area_is_visible);
		});

		google.maps.event.addListener (locationInitializer.map.get (), "center_changed", function() {
			var latlng = locationInitializer.map.get ().getCenter();
			locationInitializer.geoloc.location.latitude = latlng.lat ();
			locationInitializer.geoloc.location.longitude = latlng.lng ();

			moved = true;

			$scope.$apply(function () {
				$scope.location = locationInitializer.geoloc.location;
				$scope.clicked = $scope.location;
			});

		});


		var timerId;
		var set_search_location = function (event) {
			timerId = window.setTimeout (function () {
			
			locationInitializer.map.get ().setCenter(event.latLng);

			boundsCircle.setCenter (event.latLng);
			boundsCircle.updateStatus (search_area_is_visible);

			ADT_google_reverse_lookup (event.latLng.lat (), event.latLng.lng (), function (response) {
					var rlu = new ADT_GoogleReverseLookup (response);
					var clicked = rlu.location ().result;

					clicked.latitude = event.latLng.lat ();
					clicked.longitude = event.latLng.lng ();



					$scope.$apply(function () {
						$scope.clicked = clicked;
					});

				});

			}, 250);

		};

		google.maps.event.addListener (locationInitializer.map.get (), "click", set_search_location);
		boundsCircle.addClickListener (set_search_location);

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


	$scope.centre_map_at = function () {
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

	$scope.make_default_location = function () {
		profileService.setUserLocation ($scope.location);
	}

	$scope.places_array = [];

	$scope.search_places = function () {

		service = locationInitializer.map.placesService;

		var sel_types = [];
		if (!$scope.search.selected_type || $scope.search.selected_type == "all") {
			sel_types = $scope.types;
		} else {
			sel_types.push ($scope.search.selected_type);
		}	

		var request = {
			location: new google.maps.LatLng ($scope.clicked.latitude, $scope.clicked.longitude),
			radius: boundsCircle.getRadius ()
		};

		request.types = sel_types;

		$scope.places_array = [];
		service.nearbySearch(request, function (results, status) {
			if (status == google.maps.places.PlacesServiceStatus.OK) {
				$scope.$apply(function () {
					for (var i = 0; i < results.length; i++) {
						var place = results[i];
						$scope.places_array.push (place);
					}
				
			        });		
				
			}
		});

	};

	$scope.show_search_area = function () {
		search_area_is_visible = !search_area_is_visible;
		boundsCircle.updateStatus (search_area_is_visible);	
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


	$scope.open_marker_modal = function (obj, show_add_button) {
		$scope.marker_content = obj;
		
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
					return locationInitializer.map.get ();
				}
		    	},
		    	scope: $scope 
		});

		modalInstance.result.then(function () {
			
		}, function () {
			console.log ('Modal dismissed');
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
		var obj = {};

		for (var index in location) {
			if (location.hasOwnProperty (index)) {
				obj[index] = location[index];
			}
		}

		if (!obj.geometry) {
			obj.geometry = {
				location: {
					d: obj.latitude,
					e: obj.longitude
				}
			};

			obj.name = $("#pac_input").val();
			obj.vicinity = obj.address;
			obj.types= [];
		}

		for (var index in $scope.markers) {
			if (angular.equals ($scope.markers[index].geometry, obj.geometry)) {
				return;
			}
		}

		for (var index in $scope.current_creation_day.places) {
			var saved_place = $scope.current_creation_day.places[index];
			if (angular.equals (obj.geometry, saved_place.geometry)) {
				return;
			}
		}

		if (!obj.name || obj.name == "") {
			obj.name = "unnamed";
		}

		if (!obj.comments) {
			obj.comments = "";
		}


		obj.marker = new google.maps.Marker({
			position: new google.maps.LatLng (obj.geometry.location.d, obj.geometry.location.e),
		    	map: locationInitializer.map.get ()
		});

		google.maps.event.addListener (obj.marker, "click", function () {
			$scope.open_marker_modal (obj, true)

		});

		safeApply ($scope, function () {
			$scope.markers.push (obj);
		});
	};

	$scope.creation_remove = function (place) {
		var tmp_places = [];

		for (index in $scope.current_creation_day.places) {
			var saved_place = $scope.current_creation_day.places[index];
			if (place == saved_place) {
				place.marker.setMap (null);
			} else {
				tmp_places.push (saved_place);
			}
		}

		$scope.current_creation_day.places = tmp_places;
	};

	$scope.creation_moveup = function (place) {
		var places = $scope.current_creation_day.places;
		for (index in places) {
			var saved_place = places[index];
			if (place == saved_place) {
				if (index != 0) {
					ADT_swap_with_prev (places, index);
					break;
				} else {
					return;
				}
			}
		}

		$scope.current_creation_day.places = places;
	};

	$scope.creation_movedown = function (place) {
		var places = $scope.current_creation_day.places;
		var last_index = places.length - 1;
		for (index in places) {
			var saved_place = places[index];
			if (place == saved_place) {
				if (index != last_index) { 
					ADT_swap_with_next (places, index);
					break;
				} else {
					return;
				}
			}
		}

		$scope.current_creation_day.places = places;
	};

	$scope.my_days = [];
	$scope.creation_alerts = [];
	$scope.creation_save = function () {
		var ok = true;
		$scope.creation_alerts = [];

		var title = ADT_string_trim ($scope.current_creation_day.title);
		if (title == "") {
			$scope.creation_alerts.push ({
				type: 'danger', 
				msg: 'Error: A title is required to identify your day.'
			});

			ok = false;
		}
		var description = ADT_string_trim ($scope.current_creation_day.description);
		if (description == "") {
			$scope.creation_alerts.push ({
				msg: 'Warning: A description helps others search for your day.'
			});

		}

		console.log ($scope.creation_alerts);

		if (ok) {
			console.log (title, description);
			$scope.my_days.push (ADT_shallow_copy ($scope.current_creation_day));		
		}

	};

	$scope.creation_clear = function () {
		$scope.current_creation_day.title = "";
		$scope.current_creation_day.description = "";
		$scope. creation_alerts = [];
		for (var index in $scope.current_creation_day.places) {
			$scope.current_creation_day.places[index].marker.setMap (null);
		}

		$scope.current_creation_day.places = [];
	};

	$scope.edit_saved_day = function (day) {
		console.log ("Day", day);
		safeApply($scope, function () {
			$scope.current_creation_day = day;
			for (var index in $scope.current_creation_day.places) {
				$scope.current_creation_day.places[index].marker.setMap (
					locationInitializer.map.get ()
				);
			}
		});

	};

	$scope.creation_close_alert = function (index) {
		$scope.alerts.splice(index, 1);
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
		var place = {};
		for (var index in marker_content) {
			if (marker_content.hasOwnProperty (index)) {
				if (index != "marker") {
					place[index] = marker_content[index]; 
				}
			}
		}

		for (var index in $scope.current_creation_day.places) {
			var saved_place = $scope.current_creation_day.places[index];
			if (angular.equals (place, saved_place)) {
				return;
			}
		}

		$scope.remove_marker(marker_content);
		place.marker = new google.maps.Marker({
			position: new google.maps.LatLng (place.geometry.location.d, place.geometry.location.e),
			map: map
		});
		var iconFile = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'; 
		place.marker.setIcon(iconFile);
		google.maps.event.addListener (place.marker, "click", function () {
	        	$scope.open_marker_modal (place, false)
	        });

		$scope.current_creation_day.places.push (place);
		$modalInstance.close();
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

//	ADT_set_element_positions (width, height);

	ADT_set_section_height (height);
})


$(function () {

	var width = $(window).width();
	var height = $(window).height();
	
	ADT_set_section_height (height);
//	ADT_set_element_positions (width, height);
	console.log (width + " " + height);

});



