package com.smartparking.entity;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;


@Document(collection = "ward")
public class WardEntity {
	@Id
	private String id;
	
	@Field(value = "name")
	private String name;
	
	@Field(value = "type")
	private String type;
	
	@Field(value = "location")
	private String location;
	
	@Field(value = "id_district")
	private String idDistrict;

	private DistrictEntity district;
	
	private List<AddressEntity> addresses = new ArrayList<AddressEntity>();


	public WardEntity() {
		super();
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public DistrictEntity getDistrict() {
		return district;
	}

	public void setDistrict(DistrictEntity district) {
		this.district = district;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public List<AddressEntity> getAddresses() {
		return addresses;
	}

	public void setAddresses(List<AddressEntity> addresses) {
		this.addresses = addresses;
	}

	public String getIdDistrict() {
		return idDistrict;
	}

	public void setIdDistrict(String idDistrict) {
		this.idDistrict = idDistrict;
	}

	
	

}
