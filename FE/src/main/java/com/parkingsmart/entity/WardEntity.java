package com.parkingsmart.entity;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;

@Entity(name="ward")
public class WardEntity {
	@Id
	private String id;
	
	@Column
	private String name;
	
	@Column
	private String type;
	
	@Column
	private String location;
	
	@ManyToOne
	@JoinColumn(name="idDistrict")
	private DistrictEntity district;
	
	@OneToMany(mappedBy = "wardAddress")
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

	
	

}
