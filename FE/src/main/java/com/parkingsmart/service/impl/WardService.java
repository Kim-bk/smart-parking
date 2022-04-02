package com.parkingsmart.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.parkingsmart.dto.DistrictDTO;
import com.parkingsmart.dto.WardDTO;
import com.parkingsmart.entity.WardEntity;
import com.parkingsmart.mapper.DistrictMapper;
import com.parkingsmart.mapper.WardMapper;
import com.parkingsmart.repository.WardRepository;
import com.parkingsmart.service.IWardService;

@Service
public class WardService implements IWardService{

	@Autowired
	private WardRepository repository;
	
	@Autowired
	private WardMapper mapper;
	
	@Autowired
	private DistrictService districtService;
	
	@Autowired
	private DistrictMapper districtMapper;
	
	@Override
	public List<WardDTO> findByDistrict(String id) {
		DistrictDTO district = districtService.findById(id);
		List<WardDTO> list = new ArrayList<WardDTO>();
		if (district!=null) {
			List<WardEntity> wards = repository.findByDistrict(districtMapper.toEntity(district));
			for (WardEntity item:wards) {
				list.add(mapper.toDTO(item));
			}
		}
		return list.isEmpty()?null:list;
	}

	@Override
	public WardDTO findOneById(String id) {
		Optional<WardEntity> ward = repository.findById(id);
		if (ward.isPresent()) {
			WardDTO dto = mapper.toDTO(ward.get());
			return dto;
		}
		return null;
	}

}
