package com.smartparking.entity;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection  = "district")
public class DistrictEntity {
	
	@Id
	private String id;
	
	@Field(value = "name")
	private String name;

	@Field(value = "location")
	private String location;
	
	@Field(value = "type")
	private String type;
	
	private ProvinceEntity province;
	
	@Field(value = "id_province")
	private String idProvince;
	
	private List<WardEntity> wards = new ArrayList<WardEntity>();
	
	private List<AddressEntity> addresses = new ArrayList<AddressEntity>();


	public DistrictEntity() {
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

	public ProvinceEntity getProvince() {
		return province;
	}

	public void setProvince(ProvinceEntity province) {
		this.province = province;
	}

	public List<WardEntity> getWards() {
		return wards;
	}

	public void setWards(List<WardEntity> wards) {
		this.wards = wards;
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

	public String getIdProvince() {
		return idProvince;
	}

	public void setIdProvince(String id_province) {
		this.idProvince = id_province;
	}

	
	
	
	

}
